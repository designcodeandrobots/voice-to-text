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

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install faster-whisper tqdm
```

Download the model files from [mobiuslabsgmbh/faster-whisper-large-v3-turbo](https://huggingface.co/mobiuslabsgmbh/faster-whisper-large-v3-turbo) and place them in the `models/` folder:

```
models/
├── model.bin
├── config.json
├── tokenizer.json
├── preprocessor_config.json
└── vocabulary.json
```

## Usage

**Option 1 — double-click:** run `run.command` in Finder.

**Option 2 — terminal:**
```bash
caffeinate -i .venv/bin/python3 transcribe.py
```

Drop your `.mp3` files into `input/` and transcribed `.txt` files will appear in `output/`.

## Model

| Model | Size | Quality |
|---|---|---|
| `large-v3-turbo` | ~1.6 GB | near large-v3 accuracy, faster |

Language is set to Russian (`ru`). To change it, edit `language="ru"` in `transcribe.py`.
