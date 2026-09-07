import asyncio
from turtle import right
import edge_tts
import os
import re
import socket
import subprocess
import sys

# Ensure dependencies are present
try:
    from tenacity import retry, stop_after_attempt, wait_exponential
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tenacity"])
    from tenacity import retry, stop_after_attempt, wait_exponential

# --- Configuration ---
OUTPUT_DIR = "."
VOICE = "en-US-BrianNeural"


def clean_text_for_tts(text):
    text = re.sub(r'/[^/\s]{2,}/', '', text)
    text = re.sub(r'\[[^\]]+\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
async def save_tts(text, filename, voice, rate, pitch):
    clean_text = clean_text_for_tts(text)
    communicate = edge_tts.Communicate(
        clean_text, voice, rate=rate, pitch=pitch)
    await communicate.save(os.path.join(OUTPUT_DIR, filename))
    print(f"✅ Saved: {filename}")


async def generate_audio_pair(term, definition, index):
    # Verify connectivity
    try:
        socket.create_connection(("speech.platform.bing.com", 443), timeout=5)
    except OSError:
        print("❌ Critical: Cannot reach Microsoft TTS servers. Check your network/VPN.")
        return

    await save_tts(term, f"term{index}.mp3", VOICE, "-5%", "-5Hz")
    await save_tts(definition, f"def{index}.mp3", VOICE, "-5%", "-5Hz")

if __name__ == "__main__":
    trim = """
I was impressed by her eloquence.

"""
    dec = """

eloquent.
giving a clear, strong message:
She made an eloquent appeal for action.
Related words: eloquence, eloquently.


"""
    number = 50

    asyncio.run(generate_audio_pair(trim, dec, number))

# Python Execution_of_Item.py  ||  cd .\V\Audio\code_helper  ||
