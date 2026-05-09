# Toucan-Giant Developer Guide

This guide provides technical details about the Toucan-Giant project, including its data models, views, and integration with Google Cloud services.

## Architecture Overview

Toucan-Giant is a Django-based web application designed to facilitate the correction of transcriptions for audio files. It follows the standard Model-View-Template (MVT) architecture.

### Main Components
- **`text_corrector`**: The core application for managing audio files and their transcriptions.
- **`google_cloud_speech`**: Handles integration with Google Cloud Text-to-Speech and Speech-to-Text APIs.
- **`filemanager`**: The project configuration directory containing settings and root URL routing.

## Data Models

### TextCorrector Models (`text_corrector/models.py`)

#### `WaveText`
Represents an audio file and its associated transcriptions.
- `name`: File name (e.g., `audio01`).
- `before_normalization`: The raw transcript that needs correction.
- `after_normalization`: A processed version of the transcript (read-only in typical workflow).
- `modified`: Boolean flag indicating if the transcript has been verified/corrected.

#### `CsvFile`
Used to manage the paths of CSV files containing initial data for the database.
- `file_path`: Absolute path to the CSV file.

## Key Workflows & Code Examples

### 1. Database Population from CSV
Initial data is imported via the Django Admin panel. The expected CSV format is:
`filename|raw_text|normalized_text`

```python
# Internal logic for reading CSV (text_corrector/admin.py)
def csv_reader_and_database_filler(self, file_name):
    for row in open(file_name, "r"):
        podzielone = row.strip().split("|")
        new_record_from_wave = WaveText(
            name=podzielone[0],
            before_normalization=podzielone[1],
            after_normalization=podzielone[2],
        )
        new_record_from_wave.save()
```

### 2. Google Cloud Speech-to-Text
The application can transcribe audio using Google's API.

```python
# google_cloud_speech/views.py
from google.cloud import speech_v1

def speech_to_text(request, local_file_path):
    client = speech_v1.SpeechClient()
    language_code = "pl-PL"
    
    with io.open(local_full_path, "rb") as f:
        content = f.read()
    audio = {"content": content}
    config = {"language_code": language_code, "encoding": "LINEAR16"}

    response = client.recognize(config, audio)
    # Process response.results...
```

### 3. Google Cloud Text-to-Speech
Synthesizing speech from text input.

```python
# google_cloud_speech/views.py
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()
synthesis_input = texttospeech.SynthesisInput(text="Sample text")
voice = texttospeech.VoiceSelectionParams(language_code="pl-PL", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
```

## API Endpoints

| App | Endpoint | Description |
| :--- | :--- | :--- |
| `text_corrector` | `/` | Home page |
| `text_corrector` | `/lista-wave-tekst` | List of audio files for editing |
| `text_corrector` | `/wave-tekst/<pk>/edycja/` | Edit form for a specific transcript |
| `google_speech` | `/google-speech/text-to-speech/` | Synthesize speech from text |
| `google_speech` | `/google-speech/speech-to-text/<path>/` | Transcribe audio file |

## Configuration Notes

- **Static Files**: The `STATICFILES_DIRS` in `settings.py` may need adjustment depending on your local deployment path.
- **Media Files**: Audio files are expected in the `data_dir` (defined as `MEDIA_ROOT`).
- **Credentials**: Ensure the Google Cloud JSON key is present in `data_dir`.
