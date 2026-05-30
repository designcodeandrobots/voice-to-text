#!/bin/bash
cd "$(dirname "$0")"
caffeinate -i .venv/bin/python3 transcribe.py
echo ""
echo "Нажми Enter для закрытия..."
read
