import os
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment
import math

# Load environment variables from .env file
load_dotenv()

client = OpenAI()

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB in bytes

def get_audio_segment(file_path):
    return AudioSegment.from_file(file_path)

def calculate_chunk_duration(file_size, audio_duration, max_size):
    return int((max_size / file_size) * audio_duration)

def export_audio_chunk(audio_chunk, output_path):
    audio_chunk.export(output_path, format="mp3")

def create_audio_chunks(audio, chunk_duration_ms, file_path):
    chunks = []
    num_chunks = math.ceil(len(audio) / chunk_duration_ms)
    
    for i in range(num_chunks):
        start = i * chunk_duration_ms
        end = min((i + 1) * chunk_duration_ms, len(audio))
        
        chunk = audio[start:end]
        chunk_path = f"{file_path}_chunk_{i+1}.mp3"
        export_audio_chunk(chunk, chunk_path)
        chunks.append(chunk_path)
    
    return chunks

def chunk_audio(file_path, chunk_size=MAX_FILE_SIZE):
    file_size = os.path.getsize(file_path)
    
    if file_size <= chunk_size:
        print(f"File size is within limit. No need to split {file_path}.")
        return [file_path]
    
    print(f"File size exceeds limit. Splitting {file_path} into chunks...")
    
    audio = get_audio_segment(file_path)
    chunk_duration_ms = calculate_chunk_duration(file_size, len(audio), chunk_size)
    chunks = create_audio_chunks(audio, chunk_duration_ms, file_path)
    
    print(f"Audio split into {len(chunks)} chunks.")
    return chunks

def transcribe_audio(file_path):
    print(f"Transcribing {file_path}...")
    with open(file_path, "rb") as audio_file:
        return client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )

def join_transcripts(transcripts):
    return " ".join(transcripts).strip()

def save_transcript(transcript, original_file_path):
    output_file = f"{os.path.splitext(original_file_path)[0]}_transcript.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transcript)
    return output_file

def cleanup_chunks(chunks):
    for chunk in chunks:
        os.remove(chunk)

def process_audio_file(file_path):
    if os.path.getsize(file_path) <= MAX_FILE_SIZE:
        print("File size is within limit. Transcribing...")
        return transcribe_audio(file_path)
    
    print("File size exceeds limit. Processing in chunks...")
    chunks = chunk_audio(file_path)
    transcripts = [transcribe_audio(chunk) for chunk in chunks]  
    transcript = join_transcripts(transcripts)
    
    print("Cleaning up temporary chunk files...")
    cleanup_chunks(chunks)
    
    return transcript

def main(file_path):
    print(f"Starting transcription process for {file_path}")
    
    transcript = process_audio_file(file_path)
    
    output_file = save_transcript(transcript, file_path)
    
    print("Transcription process complete.")
    return output_file

if __name__ == "__main__":
    print("Starting audio transcription...")
    output_file = main("Publicis-Spotify-Interview.m4a")
    print(f"Transcript saved to: {output_file}")