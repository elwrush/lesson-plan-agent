import argparse
import base64
import mimetypes
import os
import struct
import sys
from google import genai
from google.genai import types

def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"File saved to: {file_name}")

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Generates a WAV file header for the given audio data."""
    # Simple PCM header generation for raw audio
    # Assuming 24kHz mono 16-bit based on user snippet default or common Gemini output
    # For robust production we might rely on the API's format, but user snippet had this logic.
    # We will use the logic provided in user snippet.
    
    bits_per_sample = 16
    rate = 24000
    
    # Try to parse from mime-type if possible, else default
    if "rate=" in mime_type:
        try:
            rate = int(mime_type.split("rate=")[1].split(";")[0])
        except:
            pass

    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", chunk_size, b"WAVE", b"fmt ", 16, 1, num_channels, sample_rate, byte_rate, block_align, bits_per_sample, b"data", data_size
    )
    return header + audio_data

def generate_audio(word, context_sentence, output_path):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    
    # Construct the strict pattern prompt
    # "pronounces word pause 1 second pronounces word pause 1 second says the example"
    prompt_text = f"Read the following with a 1-second pause between the items. Read in a warm, clear, friendly teaching voice:\n\n{word} ... ... {word} ... ... {context_sentence}"

    print(f"Generating audio for: {word}") 

    model = "gemini-2.5-pro-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt_text)],
        ),
    ]
    
    config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Leda")
            )
        ),
    )

    # Use non-streaming for simple CLI script to get the whole file
    # Or keep streaming if that's the only supported info. User used stream.
    
    output_data = b""
    mime_type = "audio/wav" # Default

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
            part = chunk.candidates[0].content.parts[0]
            if part.inline_data and part.inline_data.data:
                output_data += part.inline_data.data
                mime_type = part.inline_data.mime_type or mime_type

    if output_data:
        # Convert to WAV if needed (Gemini often returns raw PCM or similar)
        # The user's code suggests raw PCM needing a WAV header
        final_wav = convert_to_wav(output_data, mime_type)
        save_binary_file(output_path, final_wav)
    else:
        print("No audio data generated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate vocab audio using Gemini TTS")
    parser.add_argument("--word", required=True, help="The target word")
    parser.add_argument("--context", required=True, help="The context sentence")
    parser.add_argument("--output", required=True, help="Output wav file path")
    args = parser.parse_args()

    generate_audio(args.word, args.context, args.output)
