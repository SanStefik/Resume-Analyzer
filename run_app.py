import os
import webbrowser
import subprocess
import time

# Путь к вашему виртуальному окружению
venv_activate = os.path.join("venv", "Scripts", "activate.bat")

# Команда для запуска Streamlit
command = f'streamlit run app.py'

# Открытие браузера чуть позже
def open_browser():
    time.sleep(2)  # Ждём немного, чтобы сервер успел стартовать
    webbrowser.open("http://localhost:8501")

# Запускаем Streamlit из активированного окружения
subprocess.Popen(f'cmd /k "{venv_activate} && {command}"', shell=True)

# Открываем в браузере
open_browser()
