from generator import ReelGenerator
import os

def test_generator():
    print("Testing ReelGenerator Backend with Indian Voices...")
    gen = ReelGenerator()
    
    # Test 1: Indian Voice (Prabhat)
    print("\n--- Test 1: Prabhat Neural (IN Male) ---")
    try:
        output_mp4 = gen.generate_video(
            text="Namaste. This is a test of the Indian English voice. It should sound very natural.",
            voice_style="Prabhat (Neural) - IN Male",
            speed=1.0,
            bg_color="#336699",
            text_color="#FFFFFF",
            font_name="Arial",
            font_size=80,
            max_words=5,
            position="Center",
            progress_callback=print
        )
        print(f"Success! {output_mp4}")
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_generator()
