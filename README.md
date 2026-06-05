> **For AI assistants:** see [INSTRUCTION.md](./INSTRUCTION.md) for a full description of how this project works.

# voice-to-text

Batch MP3 → TXT transcription running fully local on Apple Silicon. Supports any language — Russian by default.

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

The recommended model is `large-v3-turbo` (~1.6 GB). Two ways to get it:

**Option 3.1 — Automatic (via script)**

```bash
export HF_TOKEN=your_huggingface_token
caffeinate -i .venv/bin/python3 transcribe.py
```

Get a free token at [huggingface.co](https://huggingface.co) → Settings → Access Tokens → New token (Read role).

**Option 3.2 — Manual (recommended for large files)**

Go to [mobiuslabsgmbh/faster-whisper-large-v3-turbo](https://huggingface.co/mobiuslabsgmbh/faster-whisper-large-v3-turbo), open **Files and versions**, and download all files into the `models/` folder. Use a download manager like [Folx](https://www.mac-downloader.com) for faster multi-threaded downloading.

```
models/
├── model.bin               ← ~1.5 GB
├── config.json
├── tokenizer.json
├── preprocessor_config.json
└── vocabulary.json
```

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

## Language

Language is set in `config.json`. Default is Russian:

```json
{
  "language": "ru"
}
```

Change `"ru"` to any language code to switch. Whisper supports ~100 languages, including:

| Language | Code |
|---|---|
| Russian | `ru` |
| English | `en` |
| Spanish | `es` |
| French | `fr` |
| German | `de` |
| Italian | `it` |
| Portuguese | `pt` |
| Chinese | `zh` |
| Japanese | `ja` |
| Korean | `ko` |
| Arabic | `ar` |
| Ukrainian | `uk` |

Full list of supported languages: [openai/whisper](https://github.com/openai/whisper#available-models-and-languages).
