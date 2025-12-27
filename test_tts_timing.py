import asyncio
import edge_tts

async def test_timing():
    text = "Hello world this is a test"
    voice = "en-US-GuyNeural"
    communicate = edge_tts.Communicate(text, voice)
    
    # We want to see if we can get timing information.
    # Usually capturing the stream allows us to see 'WordBoundary' events if supported
    # or we can generate subtitles.
    
    submaker = edge_tts.SubMaker()
    
    with open("tts_log.txt", "w") as f:
        async for chunk in communicate.stream():
            f.write(f"Chunk Type: {chunk['type']}\n")
            if chunk["type"] == "WordBoundary":
                f.write(f"WordBoundary: {chunk}\n")
                submaker.feed(chunk)
        
        f.write(f"SubMaker attributes: {dir(submaker)}\n")

if __name__ == "__main__":
    try:
        asyncio.run(test_timing())
    except Exception as e:
        print(f"Error: {e}")
