import re

def hex_to_rgb(hex_color):
    """Converts hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def estimate_duration(text):
    """Estimates audio duration based on word count (approx 150 wpm)."""
    words = len(text.split())
    # 150 words per minute = 2.5 words per second
    seconds = words / 2.5
    return round(seconds, 1)

def split_text_into_chunks(text, max_words=5):
    """Splits text into chunks of max_words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i:i + max_words]))
    return chunks
