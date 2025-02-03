import os
import sys
import logging
from PySide6.QtWidgets import QApplication
from app.init import MainWindow
import json
from app.config import LOGS_DIR
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
