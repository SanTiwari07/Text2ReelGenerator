import asyncio
import os
import random
import tempfile
import edge_tts
from moviepy import ColorClip, CompositeVideoClip, AudioFileClip, TextClip, ImageClip
from utils import split_text_into_chunks, hex_to_rgb
import numpy as np

# Ensure temp dir exists
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

class ReelGenerator:
    def __init__(self):
        # Expanded Neural Voice Library (Microsoft Edge TTS)
        self.voices = {
            # US English - Male
            "Guy (Neural) - US Male": "en-US-GuyNeural",
            "Christopher (Neural) - US Male": "en-US-ChristopherNeural",
            "Andrew (Neural) - US Male": "en-US-AndrewNeural",
            "Eric (Neural) - US Male": "en-US-EricNeural",
            "Brian (Neural) - US Male": "en-US-BrianNeural",
            "Steffan (Neural) - US Male": "en-US-SteffanNeural",
            
            # US English - Female
            "Jenny (Neural) - US Female": "en-US-JennyNeural",
            "Aria (Neural) - US Female": "en-US-AriaNeural",
            "Ava (Neural) - US Female": "en-US-AvaNeural",
            "Ana (Neural) - US Child/Female": "en-US-AnaNeural",
            "Michelle (Neural) - US Female": "en-US-MichelleNeural",
            
            # British - Male
            "Ryan (Neural) - UK Male": "en-GB-RyanNeural",
            
            # British - Female
            "Sonia (Neural) - UK Female": "en-GB-SoniaNeural",
            
            # Indian - Male
            "Prabhat (Neural) - IN Male": "en-IN-PrabhatNeural",
            
            # Indian - Female
            "Neerja (Neural) - IN Female": "en-IN-NeerjaNeural"
        }
        
        # Font Mapping (Windows/Linux safe fallbacks)
        self.fonts = {
            "Arial": "arial.ttf",
            "Arial Bold": "arialbd.ttf",
            "Times New Roman": "times.ttf",
            "Courier New": "cour.ttf",
            "Verdana": "verdana.ttf",
            "Georgia": "georgia.ttf",
            "Impact": "impact.ttf",
            "Comic Sans": "comic.ttf"
        }

    async def generate_audio(self, text, voice_key, rate_str="+0%"):
        """Generates TTS audio file using edge-tts."""
        # Default fallback
        voice = self.voices.get(voice_key, "en-US-GuyNeural")
        
        # If user passed a direct code (rare case), use it, otherwise lookup
        if voice_key not in self.voices and "-" in voice_key:
             voice = voice_key
             
        output_path = os.path.join(TEMP_DIR, "voice.mp3")
        communicate = edge_tts.Communicate(text, voice, rate=rate_str)
        await communicate.save(output_path)
        return output_path

    def create_text_clip_pil(self, words_to_show, highlight_idx, highlight_color, fontsize, color, font_name_key, size, position_y_offset=0):
        """Generates a text clip using PIL. Supports highlighting a specific word."""
        from PIL import Image, ImageDraw, ImageFont
        
        W, H = size
        img = Image.new('RGBA', (W, H), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Load Font
        font_file = self.fonts.get(font_name_key, "arial.ttf")
        try:
            font = ImageFont.truetype(font_file, fontsize)
        except OSError:
            try:
                font = ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
            except OSError:
                font = ImageFont.load_default()

        # Wrap text logic (Word by word to track positions)
        max_width = W - 100
        lines = [] # List of list of (word_string, original_index)
        current_line = []
        
        for idx, word in enumerate(words_to_show):
            # Check length with new word
            test_line_words = [w[0] for w in current_line] + [word]
            test_line_str = ' '.join(test_line_words)
            
            bbox = draw.textbbox((0, 0), test_line_str, font=font)
            w_line = bbox[2] - bbox[0]
            
            if w_line <= max_width:
                current_line.append((word, idx))
            else:
                lines.append(current_line)
                current_line = [(word, idx)]
        lines.append(current_line)
        
        # Draw Text
        total_text_height = len(lines) * (fontsize + 10)
        
        if position_y_offset == 'center':
            y_start = (H - total_text_height) // 2
        else:
            y_start = position_y_offset
            
        current_y = y_start
        for line_words in lines:
            # Reconstruct string for centering
            line_str = " ".join([w[0] for w in line_words])
            bbox = draw.textbbox((0, 0), line_str, font=font)
            w_line = bbox[2] - bbox[0]
            x_pos = (W - w_line) // 2
            
            # Draw each word
            # Note: We need to draw word by word to change colors, OR distinct "draw calls" if we can calculate X.
            # To avoid irregular spacing issues with manual kerning, it's safer/easier to:
            # 1. Draw the whole line stroke first (black).
            # 2. Draw the whole line main color (white/text_color).
            # 3. Draw ONLY the highlighted word in highlight_color ON TOP (if active).
            
            stroke_width = 2
            stroke_color = "black"

            # Draw Base Line (Stroke + Fill)
            for adj_x in range(-stroke_width, stroke_width+1):
                for adj_y in range(-stroke_width, stroke_width+1):
                    draw.text((x_pos+adj_x, current_y+adj_y), line_str, font=font, fill=stroke_color)
            
            # Draw Main Fill (Text Color) - But wait, if we draw normal text, we might overdraw?
            # Actually, let's just draw word by word for color control.
            # We need correct X spacing. 'draw.text' doesn't return cursor x.
            # We can calculate it.
            
            cursor_x = x_pos
            for i, (word, orig_idx) in enumerate(line_words):
                # determine color
                final_color = highlight_color if orig_idx == highlight_idx else color
                
                # Draw just this word
                draw.text((cursor_x, current_y), word, font=font, fill=final_color)
                
                # Advance cursor
                # Measure this word + space
                word_bbox = draw.textbbox((0, 0), word, font=font)
                word_w = word_bbox[2] - word_bbox[0]
                
                cursor_x += word_w
                
                # Add space width unless last word
                if i < len(line_words) - 1:
                    space_bbox = draw.textbbox((0, 0), " ", font=font)
                    space_w = space_bbox[2] - space_bbox[0]
                    cursor_x += space_w
                    
            current_y += (fontsize + 10)
            
        return ImageClip(np.array(img)).with_duration(1)

    def generate_video(self, text, voice_style, speed, bg_color, text_color, highlight_color, font_name, font_size, max_words, position, progress_callback=None):
        """Main pipeline to generate the video."""
        
        is_transparent = bg_color is None or bg_color == "Transparent"
        
        # 1. Generate Voice
        if progress_callback: progress_callback("Generating Voice...")
        
        rate_val = int((speed - 1.0) * 100)
        rate_str = f"{rate_val:+d}%"
        
        audio_path = asyncio.run(self.generate_audio(text, voice_style, rate_str))
        
        # 2. Analyze Audio
        if progress_callback: progress_callback("Analyzing Audio & Timing...")
        audio_clip = AudioFileClip(audio_path)
        total_duration = audio_clip.duration
        
        # 3. Prepare Captions & Timings
        # Estimate duration per word based on characters
        all_words = text.split()
        if not all_words: return None
        
        total_chars = sum(len(w) for w in all_words)
        # Avoid div by zero
        if total_chars == 0: total_chars = 1
        
        char_duration = total_duration / total_chars
        
        # Create Chunks
        chunks_of_words = []
        for i in range(0, len(all_words), max_words):
            chunks_of_words.append(all_words[i:i+max_words])
            
        # 4. Create Video Components
        if progress_callback: progress_callback("Compositing Video...")
        
        w, h = 1080, 1920
        
        if is_transparent:
            bg_clip = ColorClip(size=(w, h), color=(0,0,0,0), duration=total_duration, is_mask=False)
        else:
            bg_rgb = hex_to_rgb(bg_color)
            bg_clip = ColorClip(size=(w, h), color=bg_rgb, duration=total_duration)
        
        clips = [bg_clip]
        
        if position == "Center":
            y_pos_arg = 'center'
        else:
            y_pos_arg = h - 500

        current_time = 0.0
        
        for chunk in chunks_of_words:
            # Calculate duration for this chunk
            chunk_len = sum(len(w) for w in chunk)
            chunk_duration = chunk_len * char_duration
            
            # Instead of one static clip, we generate a sequence for this chunk
            # Each word in the chunk gets its moment to shine (be highlighted)
            
            # But wait, if we highlight word by word, the text of the chunk remains on screen
            # while the highlight moves.
            
            # Loop through words in this chunk and create sub-clips
            for i, word in enumerate(chunk):
                word_len = len(word)
                word_duration = word_len * char_duration
                
                # Render frame where 'i' is highlighted
                txt_img = self.create_text_clip_pil(
                    words_to_show=chunk,
                    highlight_idx=i, # Index relative to this chunk
                    highlight_color=highlight_color,
                    fontsize=font_size,
                    color=text_color,
                    font_name_key=font_name,
                    size=(w, h),
                    position_y_offset=y_pos_arg
                )
                
                txt_img = txt_img.with_start(current_time).with_duration(word_duration)
                clips.append(txt_img)
                
                current_time += word_duration

        # 5. Render
        if progress_callback: progress_callback("Rendering Final Video...")
        final_video = CompositeVideoClip(clips)
        final_video = final_video.with_audio(audio_clip)
        
        if is_transparent:
            output_filename = os.path.join(TEMP_DIR, "output_reel.webm")
            final_video.write_videofile(
                output_filename, 
                fps=24, 
                codec='libvpx-vp9',
                ffmpeg_params=['-pix_fmt', 'yuva420p'],
                logger=None
            )
        else:
            output_filename = os.path.join(TEMP_DIR, "output_reel.mp4")
            final_video.write_videofile(
                output_filename, 
                fps=24, 
                codec='libx264', 
                audio_codec='aac',
                preset='ultrafast',
                logger=None
            )
        
        return output_filename
