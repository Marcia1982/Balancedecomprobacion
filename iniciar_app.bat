@echo off
cd /d %~dp0
echo Iniciando Validador Financiero AI...
start http://localhost:5000
uv run python app/main.py
