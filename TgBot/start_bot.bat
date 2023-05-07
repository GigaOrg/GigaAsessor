@echo off

echo Installing required libraries...

pip install -r requirements.txt > nul

echo Starting Telegram-bot...

python GA3.py

pause
