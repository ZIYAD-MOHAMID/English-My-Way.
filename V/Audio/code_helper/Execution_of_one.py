import asyncio
import edge_tts
import os
import re
import socket
from tenacity import retry, stop_after_attempt, wait_exponential

# --- Configuration ---
OUTPUT_DIR = "."
VOICE = "en-US-BrianNeural"
RATE = "-5%"
PITCH = "-5Hz"


def clean_text_for_tts(text):
    text = re.sub(r'/[^/\s]{2,}/', '', text)
    text = re.sub(r'\[[^\]]+\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def check_network():
    """Checks if the Microsoft TTS server is reachable."""
    try:
        socket.create_connection(("speech.platform.bing.com", 443), timeout=5)
        return True
    except OSError:
        return False


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
async def save_tts(text, filename):
    """Generates and saves a single audio file with retry logic."""
    clean_content = clean_text_for_tts(text)
    output_path = os.path.join(OUTPUT_DIR, f"{filename}.mp3")

    communicate = edge_tts.Communicate(
        clean_content, VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(output_path)
    print(f"✅ Saved: {output_path}")


async def run_generator(text, label):
    """Main execution wrapper."""
    if not check_network():
        print("❌ Critical: Cannot reach Microsoft TTS servers. Check your network.")
        return

    try:
        await save_tts(text, label)
    except Exception as e:
        print(f"❌ Failed to generate {label} after multiple attempts: {e}")

if __name__ == "__main__":
    # Example usage:
    my_text = """
Meaning: The government controls companies using rules that matter for the economy.
-
relative.
All her relatives came to the wedding.
We considered the relative merits of flying to Washington or taking the train.
-
merit.
on its (own) merits.
Being able to work at home has its merits.
Judged on artistic merit, it was a success.
to deserve something: These recommendations merit careful attention.
-
it's relatively stacked. 
-
relevance.
the relevance of railroads to the development of the American west.
"""

    my_label = "def78"

    asyncio.run(run_generator(my_text, my_label))


# Python Execution_of_one.py  ||  cd .\V\Audio\code_helper  ||
