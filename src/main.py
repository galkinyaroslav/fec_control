import os
import sys
import logging
from PySide6.QtWidgets import QApplication
from app.init import MainWindow
import json
from app.config import LOGS_DIR, RUNS_DIR, DATA_DIR, TEMP_DIR
from pathlib import Path


def setup_logging():
    """Настройка логирования."""
    if  not LOGS_DIR.exists():
        Path.mkdir(LOGS_DIR)
    logs_file = Path(LOGS_DIR,'app.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_file),
            logging.StreamHandler(sys.stdout),
        ]
    )
def setup_data():
    """Настройка данных."""
    if  not DATA_DIR.exists():
        Path.mkdir(DATA_DIR)

def setup_runs():
    """Настройка ранов."""
    if  not RUNS_DIR.exists():
        Path.mkdir(RUNS_DIR)

def setup_temp():
    """Настройка временных файлов."""
    if  not TEMP_DIR.exists():
        Path.mkdir(TEMP_DIR)


def load_config():
    """Загрузка конфигурации из файла."""
    try:
        with open("data/config.json", "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        logging.error("Config file not found. Using default configuration.")
        return {}
    except json.JSONDecodeError:
        logging.error("Invalid JSON in config file. Using default configuration.")
        return {}

def main():
    setup_logging()
    setup_data()
    setup_runs()
    setup_temp()
    # load_config()
    # config = load_config()
    # logging.info("Configuration loaded: %s", config)

    application = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    try:
        sys.exit(application.exec())
    except Exception as e:
        logging.error("Application crashed: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
