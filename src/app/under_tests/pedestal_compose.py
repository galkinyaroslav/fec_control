from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from app.logic.data_structure.factory import NWaveForm

from app.config import RUNS_DIR, DATA_DIR
from app.logic.sampa_fit import SampaFit

def make_pedestal_data(path, firmware_version = '0x24040800'):
    all_mean_pdf = pd.DataFrame(dtype=float)
    all_rms_pdf = pd.DataFrame(dtype=float)

    files = sorted(path.rglob('*.txt'), key=lambda f: int(f.stem.split("-")[0]))
    print(f'{files=}')
    len_files = len(files)
    for entry in files:
        data = NWaveForm(Path(path,entry),firmware=firmware_version)
        mean=data.mean
        print(f'1-{mean=}')

        mean_pdf = pd.DataFrame(data.mean)
        rms_pdf = pd.DataFrame(data.rms)
        all_rms_pdf = pd.concat([all_rms_pdf, rms_pdf], ignore_index=True, axis=1)
        all_mean_pdf = pd.concat([all_mean_pdf, mean_pdf], ignore_index=True, axis=1)
    all_mean_pdf = all_mean_pdf.round(2).T
    all_rms_pdf = all_rms_pdf.round(2).T
    all_mean_pdf.index = range(1, len_files + 1)
    all_rms_pdf.index = range(1, len_files + 1)

    return all_mean_pdf, all_rms_pdf

if __name__ == '__main__':
    from matplotlib import pyplot as plt

    # CARD_NUMBER = ['309', '334', '336', '337', '338', '339', '340', '345', '363', '459',]
    # ENC = ['0pF', '10pF', '20pF', '40pF']
    # TEST_NAME = ['rms_pedestal',]
    CARD_NUMBER = ['1181', ]
    ENC = ['0pF',]
    TEST_NAME = ['rms_pedestal', ]

    # calculation = Path(f'{RUNS_DIR}/{CARD_NUMBER}/{ENC}/calculations/')
    # calculation.mkdir(parents=True, exist_ok=True)



    for card_number in CARD_NUMBER:
        for enc in ENC:
            for test_name in TEST_NAME:
                calculation = Path(f'{RUNS_DIR}/{card_number}/{enc}/calculations/')
                calculation.mkdir(parents=True, exist_ok=True)
                # calculation = Path(f'{RUNS_DIR}/calculations/pedestal')
                # calculation.mkdir(parents=True, exist_ok=True)

                path = Path(f'{RUNS_DIR}/{card_number}/{enc}/{test_name}')
                print(path)
                # path = Path(f'{RUNS_DIR}/{CARD_NUMBER}/{ENC}/{TEST_NAME}')
                # print(path)
                all_pdf = make_pedestal_data(path=path)
                all_pdf[0].to_excel(f'{calculation}/{card_number}-{enc}-{test_name}-mean2.xlsx')
                all_pdf[1].to_excel(f'{calculation}/{card_number}-{enc}-{test_name}-rms2.xlsx')


