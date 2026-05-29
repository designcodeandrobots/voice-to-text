#!/usr/bin/env .venv/bin/python3
"""
Транскрибирует все MP3 из папки input/ в TXT в папку output/.
Использует faster-whisper с моделью large-v3-turbo.
"""

import sys
from pathlib import Path

try:
    from faster_whisper import WhisperModel
    from huggingface_hub import snapshot_download
    from tqdm import tqdm
except ImportError:
    print("Установите зависимости: pip install faster-whisper tqdm")
    sys.exit(1)

MODEL_SIZE = "large-v3-turbo"
MODEL_REPO = "mobiuslabsgmbh/faster-whisper-large-v3-turbo"

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")


def download_model():
    print(f"Скачиваю модель {MODEL_SIZE} (~1.6 GB)...")
    snapshot_download(
        repo_id=MODEL_REPO,
        local_dir=None,
        tqdm_class=tqdm,
    )
    print("Модель скачана.\n")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    mp3_files = sorted(INPUT_DIR.glob("*.mp3"))
    if not mp3_files:
        print(f"Нет MP3-файлов в папке {INPUT_DIR}/")
        return

    todo = [f for f in mp3_files if not (OUTPUT_DIR / (f.stem + ".txt")).exists()]
    done = [f for f in mp3_files if (OUTPUT_DIR / (f.stem + ".txt")).exists()]

    if done:
        print(f"Уже готово ({len(done)}):")
        for f in done:
            print(f"  ✓ {f.name}")
    print(f"\nБудет обработано: {len(todo)} из {len(mp3_files)}")
    if not todo:
        print("Нечего делать.")
        return
    print()

    print(f"Загружаю модель в память...")
    model = WhisperModel("models", device="cpu", compute_type="int8")

    print(f"Модель загружена. Файлов для обработки: {len(mp3_files)}\n")

    for i, audio_path in enumerate(todo, 1):
        output_path = OUTPUT_DIR / (audio_path.stem + ".txt")

        print(f"[{i}/{len(todo)}] Транскрибирую: {audio_path.name}")
        segments, info = model.transcribe(str(audio_path), language="ru", beam_size=5)
        texts = []
        with tqdm(total=round(info.duration), unit="сек", desc="  прогресс") as bar:
            pos = 0
            for segment in segments:
                texts.append(segment.text.strip())
                new_pos = round(segment.end)
                if new_pos > pos:
                    bar.update(new_pos - pos)
                    pos = new_pos
        text = " ".join(texts)
        output_path.write_text(text, encoding="utf-8")

        print(f"  Сохранено: {output_path.name}\n")

    print("Всё готово.")


if __name__ == "__main__":
    main()
