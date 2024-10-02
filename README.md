# Audio Transcription Script

This script transcribes audio files using OpenAI's Whisper model. It can handle large files by splitting them into chunks if necessary.

## Technologies Used

- **Python**: The primary programming language used.
- **OpenAI API**: For accessing the Whisper model for audio transcription.
- **pydub**: Used for audio file manipulation and chunking.
- **dotenv**: For loading environment variables.
- **os**: For file and path operations.
- **math**: For mathematical calculations in chunking process.

## How It Works

1. **Environment Setup**: 
   - Uses `dotenv` to load environment variables (likely for OpenAI API key).
   - Initializes OpenAI client.

2. **File Size Check**:
   - If file size <= 25MB, transcribes directly.
   - If file size > 25MB, splits into chunks.

3. **Chunking Process** (for large files):
   - Calculates optimal chunk duration based on file size and audio length.
   - Splits audio into chunks and saves them as temporary MP3 files.

4. **Transcription**:
   - Uses OpenAI's Whisper model to transcribe each chunk or the whole file.
   - Joins transcripts from chunks if applicable.

5. **Cleanup**:
   - Saves final transcript as a text file.
   - Removes temporary chunk files.

## Key Functions

- `get_audio_segment()`: Loads audio file using pydub.
- `calculate_chunk_duration()`: Determines optimal chunk size.
- `create_audio_chunks()`: Splits audio into chunks.
- `transcribe_audio()`: Sends audio to OpenAI for transcription.
- `process_audio_file()`: Main function handling the transcription process.

## Usage

Run the script with:

```python
python script_name.py
```


## Things to Remember

- The script uses OpenAI's API, so make sure your API key is set in the environment.
- It can handle large files by splitting them, useful for long recordings.
- The output is a plain text transcript.

## Planned Improvements

1. **Multiple File Processing**: 
   - Allow processing of multiple files by accepting a directory path.
   - Implement batch processing for efficiency.

2. **Subtitle Format Support**: 
   - Add support for SRT or VTT formats.
   - Ensure timestamps in subtitles align with original audio length.

3. **File Type Conversion**: 
   - Implement automatic conversion for unsupported file types before transcription.

4. **Speaker Diarization**: 
   - Research feasibility of identifying different speakers in the audio.
   - Implement if possible, perhaps using a different API or model.

5. **Progress Tracking**: 
   - Add a progress bar or status updates for long transcriptions.

