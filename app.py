import streamlit as st
import os
import time
import asyncio
from generator import ReelGenerator
from utils import estimate_duration

# Page Config
st.set_page_config(
    page_title="Text2Reel Professional", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Look
st.markdown("""
    <style>
    /* Global Font & Colors */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #262730;
        color: white;
        border: 1px solid #4B4B4B;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        border-color: #FF4B4B;
        background-color: #262730;
    }
    
    /* Main Generate Button */
    div[data-testid="stForm"] .stButton button {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF914D 100%);
        border: none;
        color: white;
        font-weight: bold;
        padding: 15px;
        font-size: 1.1rem;
    }
    div[data-testid="stForm"] .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
    }
    
    /* Status Box */
    .success-box {
        padding: 1rem;
        background-color: #D1FFD6;
        color: #006400;
        border-radius: 8px;
        border: 1px solid #00B300;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# sidebar Header
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3074/3074767.png", width=80)
    st.title("Text2Reel Pro 🎬")
    st.markdown("---")
    st.markdown("**Create viral short-form videos in seconds.**")
    st.markdown("1. Write Script\n2. Customize Style\n3. Export")
    st.markdown("---")
    st.info("💡 **Pro Tip**: Use 'Transparent' background to create overlays for editing software.")

# Init Generator
if 'generator' not in st.session_state:
    st.session_state.generator = ReelGenerator()

# Helper for Voice Preview
def play_voice_preview(text, voice, speed):
    """Generates and plays a quick voice sample."""
    with st.spinner(f"Generating preview for {voice}..."):
        # We need a dedicated wrapper or just use the generator's async path directly via run
        # Ideally, generator should expose a clean async wrapper, but we can do this:
        try:
            rate_val = int((speed - 1.0) * 100)
            rate_str = f"{rate_val:+d}%"
            # We use a temp method or just call generate_audio logic here
            # Re-using internal method for simplicity (hacky but works fast)
            path = asyncio.run(st.session_state.generator.generate_audio(text, voice, rate_str))
            st.audio(path)
        except Exception as e:
            st.error(f"Preview failed: {e}")

# Main Layout
st.markdown("## ⚡ Create Your Reel")

# Two-Column Layout (Script vs Output settings)
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown("### 1. Script & Voice")
    
    # Text Input
    text_input = st.text_area(
        "Enter your script", 
        placeholder="Wake up early. Grind hard. Success is waiting...",
        height=200,
        help="Type the content you want spoken and displayed."
    )
    
    # Duration & Word Count
    if text_input:
        est_time = estimate_duration(text_input)
        word_count = len(text_input.split())
        st.caption(f"📝 **{word_count} words** | ⏱️ Est. Duration: **{est_time}s**")

    st.markdown("---")
    st.markdown("### 2. Audio Settings")
    
    # Voice Controls
    c1, c2 = st.columns([3, 1])
    with c1:
        voice_options = list(st.session_state.generator.voices.keys())
        voice_key = st.selectbox("🎙️ Voice Character", voice_options, index=2) # Default excellent neutral
    
    with c2:
        speed = st.number_input("Speed", 0.5, 1.5, 1.0, 0.1)

    # Preview Button (Outside Form to allow instant interaction)
    if st.button("🔊 Preview Voice"):
        preview_text = text_input if text_input else "This is a preview of my voice. How do I sound?"
        # Limit preview length
        preview_text = " ".join(preview_text.split()[:15]) 
        play_voice_preview(preview_text, voice_key, speed)


with col_right:
    st.markdown("### 3. Visual Design")
    
    with st.container(border=True):
        # Using tabs for organized settings
        tab1, tab2 = st.tabs(["Appearance", "Layout"])
        
        with tab1:
            bg_type = st.radio("Background", ["Solid Color", "Transparent (WebM)"], horizontal=True)
            if bg_type == "Solid Color":
                bg_color = st.color_picker("Background Hex", "#1E1E1E")
            else:
                bg_color = "Transparent"
                st.caption("ℹ️ Exports as WebM with alpha channel.")
                
            text_color = st.color_picker("Text Color", "#FFFFFF")
            highlight_color = st.color_picker("Highlight Color", "#FF4B4B")
            
            font_options = ["Arial", "Arial Bold", "Times New Roman", "Courier New", "Verdana", "Georgia", "Impact", "Comic Sans"]
            font_choice = st.selectbox("Font Family", font_options, index=1)
            
        with tab2:
            font_size = st.slider("Text Size (px)", 40, 150, 80, 5)
            max_words = st.slider("Words per Chunk", 1, 10, 5, 1)
            position = st.selectbox("Vertical Align", ["Center", "Bottom"])


# Generate Actions
st.markdown("---")
gen_col1, gen_col2 = st.columns([2, 1])

with gen_col1:
    if st.button("🚀 GENERATE REEL (Render Video)", type="primary", use_container_width=True):
        if not text_input:
            st.error("Please enter a script first!")
        else:
            with st.status("🎬 Production in progress...", expanded=True) as status:
                progress_bar = st.progress(0)
                
                def p_callback(msg):
                    status.write(f"⚙️ {msg}")
                    if "Voice" in msg: progress_bar.progress(20)
                    elif "Audio" in msg: progress_bar.progress(40)
                    elif "Compositing" in msg: progress_bar.progress(70)
                    elif "Final" in msg: progress_bar.progress(90)

                try:
                    start_t = time.time()
                    output_path = st.session_state.generator.generate_video(
                        text=text_input,
                        voice_style=voice_key,
                        speed=speed,
                        bg_color=bg_color,
                        text_color=text_color,
                        highlight_color=highlight_color,
                        font_name=font_choice,
                        font_size=font_size,
                        max_words=max_words,
                        position=position,
                        progress_callback=p_callback
                    )
                    end_t = time.time()
                    
                    progress_bar.progress(100)
                    status.update(label="✅ Loop Completed!", state="complete", expanded=False)
                    
                    st.success(f"Video generated in {round(end_t - start_t, 1)}s")
                    
                    # Store output in session to persist across re-runs if needed
                    st.session_state.last_video = output_path
                    
                except Exception as e:
                    st.error(f"Generation Error: {e}")
                    status.update(label="❌ Failed", state="error")

with gen_col2:
    # Check if we have a generated video to show
    if 'last_video' in st.session_state:
        output_path = st.session_state.last_video
        
        # Determine format
        if output_path.endswith(".webm"):
             mime = "video/webm"
             ext = "webm"
        else:
             mime = "video/mp4"
             ext = "mp4"

        # Download Button
        with open(output_path, "rb") as file:
            st.download_button(
                label=f"📥 Download .{ext.upper()}",
                data=file,
                file_name=f"text2reel_output.{ext}",
                mime=mime,
                use_container_width=True
            )
        
        # Preview might need restart or distinct key to refresh
        st.video(output_path)
