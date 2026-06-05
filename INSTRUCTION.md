# INSTRUCTION.md

This file describes the voice-to-text project for AI assistants. Use it as context when helping with this codebase.

## What this project does

This is a local batch audio transcription tool. It takes MP3 files and converts them to plain text using a locally running speech recognition model. No internet connection is required during transcription. The target language is Russian.

## Project structure

```
voice-to-text/
├── transcribe.py          # main script — all logic lives here
├── run.command            # double-click launcher for macOS
├── requirements.txt       # Python dependencies
├── input/                 # drop MP3 files here
├── output/                # TXT results appear here (same filename as audio)
└── models/                # local model files (not committed to git)
    ├── model.bin
    ├── config.json
    ├── tokenizer.json
    ├── preprocessor_config.json
    └── vocabulary.json
```

## How transcribe.py works

1. Scans `input/` for `.mp3` files
2. Checks `output/` for existing `.txt` files — skips files already transcribed
3. Prints a summary: how many files are done, how many will be processed
4. Loads the Whisper model from the local `models/` folder into memory
5. Transcribes each file one by one with a progress bar showing seconds of audio processed
6. Saves the result as `output/<same-filename>.txt`

## Tech stack

- **faster-whisper** — CTranslate2-based Whisper inference, runs on CPU with int8 quantization
- **Model**: `mobiuslabsgmbh/faster-whisper-large-v3-turbo` (~1.6 GB), a distilled version of `whisper-large-v3`
- **Language**: Russian (`ru`), set via `language="ru"` in `model.transcribe()`
- **Device**: CPU with `compute_type="int8"` — optimized for Apple Silicon
- **tqdm**: progress bar during transcription
- **huggingface_hub**: used for model downloading (optional, model can be placed manually)

## Key configuration in transcribe.py

```python
MODEL_SIZE = "large-v3-turbo"                              # model name (used for display)
MODEL_REPO = "mobiuslabsgmbh/faster-whisper-large-v3-turbo"  # HuggingFace repo (for downloading)
INPUT_DIR  = Path("input")                                 # source folder
OUTPUT_DIR = Path("output")                                 # destination folder
language   = "ru"                                          # transcription language
beam_size  = 5                                             # accuracy vs speed trade-off
```

## How to change the language

Edit `language="ru"` in the `model.transcribe()` call inside `transcribe.py`. Use standard ISO 639-1 codes (e.g. `"en"`, `"de"`, `"fr"`).

## How to switch to a different model

1. Download the new model files into `models/`
2. Update `MODEL_SIZE` and `MODEL_REPO` in `transcribe.py`

Available faster-whisper models: `tiny`, `base`, `small`, `medium`, `large-v2`, `large-v3`, `large-v3-turbo`.

## run.command

A macOS shell script that:
- Changes directory to the project folder
- Runs the script with `caffeinate -i` to prevent the Mac from sleeping during transcription
- Waits for Enter before closing the Terminal window

## What is NOT in the repo

- `input/` folder contents (audio files)
- `output/` folder contents (transcription results)
- `models/` folder (model weights — too large for git)
- `.venv/` (virtual environment)

These are excluded via `.gitignore`.

## Common issues

| Problem | Likely cause | Fix |
|---|---|---|
| `No MP3 files found` | input/ folder is empty | add `.mp3` files to `input/` |
| `ModuleNotFoundError` | venv not activated or deps not installed | run `pip install faster-whisper tqdm` inside the venv |
| Model load error | `models/` folder missing or incomplete | re-download model files |
| Mac sleeps mid-run | ran without `caffeinate` | use `run.command` or prefix with `caffeinate -i` |
| File skipped unexpectedly | `.txt` already exists in `output/` | delete the `.txt` to re-transcribe |
