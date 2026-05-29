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

    print(f"Загружаю модель в память...")
    model = WhisperModel("models", device="cpu", compute_type="int8")

    print(f"Модель загружена. Файлов для обработки: {len(mp3_files)}\n")

    for i, audio_path in enumerate(mp3_files, 1):
        output_path = OUTPUT_DIR / (audio_path.stem + ".txt")

        if output_path.exists():
            print(f"[{i}/{len(mp3_files)}] Пропускаю (уже есть): {output_path.name}")
            continue

        print(f"[{i}/{len(mp3_files)}] Транскрибирую: {audio_path.name}")
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
