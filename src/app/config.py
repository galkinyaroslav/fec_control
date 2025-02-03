# import os
import sys
from pathlib import Path

if getattr(sys, "frozen", False):  # Приложение собрано в .exe
    WORKING_DIR = sys._MEIPASS
else:
    WORKING_DIR = Path(__file__).resolve().parent
    # Path(WORKING_DIR).absolute().mkdir(p
    # WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = Path(WORKING_DIR).joinpath("../config/config.json")
DATA_DIR = Path(WORKING_DIR).joinpath("../data")
RUNS_DIR = Path(DATA_DIR).joinpath("runs")
LOGS_DIR = Path(DATA_DIR).joinpath("../logs")
TEMP_DIR = Path(DATA_DIR).joinpath("../../temp")

if __name__ == "__main__":
    print(type(WORKING_DIR))
    print(DATA_DIR)
    print(RUNS_DIR)
    print(LOGS_DIR)
    print(TEMP_DIR)