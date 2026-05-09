# EchoVerse

EchoVerse is an AI-powered audiobook creator built with Python and Streamlit. It rewrites user text into a selected tone, translates it into supported languages, and generates spoken audio as an MP3 file.

## What EchoVerse Does

- Accepts user text input by pasting or uploading a `.txt` file
- Rewrites text in different tones such as Neutral, Suspenseful, Inspiring, Professional, and Casual
- Optionally translates the rewritten text into a chosen language
- Converts the final text into spoken audio using Google Text-to-Speech (`gTTS`)
- Displays an in-browser audio preview and provides an MP3 download link

## Key Components

- `app.py` — the main Streamlit application that handles the UI, text rewriting, translation, and audio generation flow
- `granite_model.py` — helper module for Hugging Face text generation integration (future API-based expansion)
- `tts_model.py` — helper module for audio generation using Hugging Face or local fallback methods
- `requirements.txt` — Python dependencies used by the project

## Technology Stack

- Python 3.13+
- Streamlit for the web interface
- Hugging Face `transformers` for text rewriting
- `torch` as the model backend for Hugging Face pipelines
- `gTTS` for MP3 audio generation
- `deep-translator` for translating text into other languages

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/Harshini-08-design/EchoVerse.git
cd EchoVerse
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. If you want to use the Hugging Face Hub with an API token, create a `.env` file and add:

```text
HF_API_TOKEN=hf_xxxYOURTOKENxxx
```

## Running the App

Launch the Streamlit application with:

```bash
streamlit run app.py
```

Then open the URL shown in your browser, typically `http://localhost:8501`.

## Usage Guide

1. Enter or upload text in the input area.
2. Choose the target language and tone.
3. Click **Generate Audiobook**.
4. View the rewritten text and listen to the generated audio.
5. Download the MP3 if desired.

## Notes

- The first time the model runs, it may take longer to load while downloading model files.
- Audio output will only read the rewritten text, not the prompt or instruction.
- The app is designed for easy expansion, with helper modules available for future API-based model or TTS upgrades.

## License

This project is provided as-is for educational and personal use.
