@echo off

echo Installing required libraries...

pip install -r requirements.txt > nul

echo Starting Discord-bot...

python main.py

pause
