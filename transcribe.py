#!/usr/bin/env .venv/bin/python3
"""
Transcribes all MP3 files from the input/ folder into TXT files in the output/ folder.
Uses faster-whisper with the large-v3-turbo model.
"""

import json
import sys
from pathlib import Path

try:
    from faster_whisper import WhisperModel
    from huggingface_hub import snapshot_download
    from tqdm import tqdm
except ImportError:
    print("Install dependencies: pip install faster-whisper tqdm")
    sys.exit(1)

MODEL_SIZE = "large-v3-turbo"
MODEL_REPO = "mobiuslabsgmbh/faster-whisper-large-v3-turbo"

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

config = json.loads(Path("config.json").read_text())
LANGUAGE = config.get("language", "ru")


def download_model():
    print(f"Downloading model {MODEL_SIZE} (~1.6 GB)...")
    snapshot_download(
        repo_id=MODEL_REPO,
        local_dir=None,
        tqdm_class=tqdm,
    )
    print("Model downloaded.\n")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    mp3_files = sorted(INPUT_DIR.glob("*.mp3"))
    if not mp3_files:
        print(f"No MP3 files found in {INPUT_DIR}/")
        return

    todo = [f for f in mp3_files if not (OUTPUT_DIR / (f.stem + ".txt")).exists()]
    done = [f for f in mp3_files if (OUTPUT_DIR / (f.stem + ".txt")).exists()]

    if done:
        print(f"Already done ({len(done)}):")
        for f in done:
            print(f"  ✓ {f.name}")
    print(f"\nTo process: {len(todo)} of {len(mp3_files)}")
    if not todo:
        print("Nothing to do.")
        return
    print()

    print("Loading model into memory...")
    model = WhisperModel("models", device="cpu", compute_type="int8")
    print(f"Model loaded. Files to process: {len(todo)}\n")

    for i, audio_path in enumerate(todo, 1):
        output_path = OUTPUT_DIR / (audio_path.stem + ".txt")

        print(f"[{i}/{len(todo)}] Transcribing: {audio_path.name}")
        segments, info = model.transcribe(str(audio_path), language=LANGUAGE, beam_size=5)
        texts = []
        with tqdm(total=round(info.duration), unit="sec", desc="  progress") as bar:
            pos = 0
            for segment in segments:
                texts.append(segment.text.strip())
                new_pos = round(segment.end)
                if new_pos > pos:
                    bar.update(new_pos - pos)
                    pos = new_pos
        text = " ".join(texts)
        output_path.write_text(text, encoding="utf-8")

        print(f"  Saved: {output_path.name}\n")

    print("All done.")


if __name__ == "__main__":
    main()
