# voice-to-text

Batch MP3 → TXT transcription for Russian audio, running fully local on Apple Silicon.

## How it works

- Reads all `.mp3` files from the `input/` folder
- Transcribes each file using [faster-whisper](https://github.com/SYSTRAN/faster-whisper) with the `large-v3-turbo` model
- Saves results as `.txt` files in the `output/` folder with the same filename
- Skips files that have already been transcribed

## Requirements

- Any Mac with M chip
- Python 3.10+

## Installation

**1. Clone the repo**
```bash
git clone https://github.com/designcodeandrobots/voice-to-text.git
cd voice-to-text
```

**2. Create a virtual environment and install dependencies**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install faster-whisper tqdm
```

**3. Download the model**

Go to [mobiuslabsgmbh/faster-whisper-large-v3-turbo](https://huggingface.co/mobiuslabsgmbh/faster-whisper-large-v3-turbo) on Hugging Face, open the **Files and versions** tab, and download these files into the `models/` folder:

```
models/
├── model.bin               ← ~1.5 GB, download this first
├── config.json
├── tokenizer.json
├── preprocessor_config.json
└── vocabulary.json
```

> Tip: use a download manager (e.g. Folx) for `model.bin` — it's large and benefits from multi-threaded downloading.

**4. Create input and output folders**
```bash
mkdir input output
```

## Usage

Drop your `.mp3` files into `input/`, then run:

**Option 1 — double-click:** run `run.command` in Finder.

**Option 2 — terminal:**
```bash
caffeinate -i .venv/bin/python3 transcribe.py
```

Transcribed `.txt` files will appear in `output/` with the same filename as the audio.

## Model

| Model | Size | Quality |
|---|---|---|
| `large-v3-turbo` | ~1.6 GB | near large-v3 accuracy, faster |

Language is set to Russian (`ru`). To change it, edit `language="ru"` in `transcribe.py`.
