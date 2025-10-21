import os
import re
from pathlib import Path

import pandas as pd
from openpyxl.styles.builtins import calculation

from app.config import DATA_DIR, RUNS_DIR
from app.logic.fec import TestsName

HEADER = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0', 'Tsam', 'Va2_1_25',
          'mA3_S1', 'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']
pd.options.display.float_format = '{:.2f}'.format

def make_vat_data(path):
    all_pdf = pd.DataFrame(dtype=float)
    files = sorted(path.rglob('*.vat'), key=lambda f: int(f.stem.split("-")[0]))
    print(f'{files=}')
    len_files = len(files)
    for entry in files:
        print(entry)
        with open(entry, 'r') as vat_file:
            data = vat_file.readlines()
            print(data)
            # Delete '\n', without HEADER, convert ot float
            pdf = pd.DataFrame([d[:-1].split(' ') for d in data[1:]], columns=HEADER, dtype=float)
            print(pdf)
            print(f"{type(pdf['T'][0])=}")
            print(f'{pdf.mean()=}')
            print(f'{len(pdf.mean())=}')
            all_pdf = pd.concat([all_pdf, pdf.mean()], ignore_index=True, axis=1)
    all_pdf=all_pdf.round(2)
    all_pdf = all_pdf.T
    all_pdf.index=range(1, len_files+1)
    return all_pdf

if __name__=='__main__':
    calculation = Path(f'{RUNS_DIR}/calculations/')
    calculation.mkdir(parents=True, exist_ok=True)

    # CARD_NUMBER = ['309', '334', '336', '337', '338', '339', '340', '345', '363', '459',]
    # ENC = ['0pF', '10pF', '20pF', '40pF']
    # TEST_NAME = ['rms_pedestal', 'gain']
    CARD_NUMBER = ['1181',]
    ENC = ['0pF',]
    TEST_NAME = ['rms_pedestal',]

    for card_number in CARD_NUMBER:
        for enc in ENC:
            for test_name in TEST_NAME:
                # calculation = Path(f'{RUNS_DIR}/{card_number}/{enc}/calculations/')
                # calculation.mkdir(parents=True, exist_ok=True)
                path = Path(f'{RUNS_DIR}/{card_number}/{enc}/{test_name}')
                print(path)
                all_pdf = make_vat_data(path=path)
                print(all_pdf)
                all_pdf.to_excel(f'{calculation}/{card_number}-{enc}-{test_name}_vat.xlsx')

    # path = Path(f'{RUNS_DIR}/{CARD_NUMBER}/{ENC}/{TEST_NAME}')
    # print(path)
    # all_pdf = make_vat_data(path=path)
    # all_pdf.to_excel(f'{calculation}/{TEST_NAME}_vat.xlsx')


