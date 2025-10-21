"""
собираем данные в 1 файл.
создается 2 файла:
    1) линейность
    2) данные события в LSB
"""
from collections import defaultdict
from pathlib import Path
import re

import numpy as np
import pandas as pd
from pandas import DataFrame
from app.config import RUNS_DIR, DATA_DIR

from app.logic.sampa_fit import SampaFit
from app.logic.data_structure.factory import NWaveForm



CARD_NUMBER = '309'
ENC = ['0pF', '10pF', '20pF', '40pF', ]
TEST_NAME = 'gain'
PARITY='EVEN'
for enc in ENC:
    calculation = Path(f'{RUNS_DIR}/{CARD_NUMBER}/{enc}/calculations/')
    calculation.mkdir(parents=True, exist_ok=True)

    # paths = Path(f'../../../data/gain/').glob('*.txt')
    path = Path(f'{RUNS_DIR}/{CARD_NUMBER}/{enc}/{TEST_NAME}')
    # files = sorted(path.rglob('*.txt'), key=lambda f: int(f.stem.split("-")[0]))
    files = [i for i in path.rglob('*.txt')]
    # [print(i) for i in files]
    # run_number = set([int(i.stem.split('-')[0]) for i in files])
    vin = sorted(set([float(i.stem.split('-')[4][:-1]) for i in files]))
    print(f'{vin=}')


    def group_files_by_run(files: list[Path]) -> dict[int, list[tuple[float,Path]]]:
        runs = defaultdict(list)
        for f in files:
            parts = f.stem.split("-")        # ['23','1181','even','2pF','1.5V']
            num = int(parts[0])              # номер рана
            val = float(parts[-1][:-1])      # "1.5V" -> 1.5
            runs[f'{num}'].append((val, f))       # временно сохраняем (val, Path)

        # сортируем и убираем val
        return {num: [(v,f) for v, f in sorted(items, key=lambda x: x[0])]
                for num, items in runs.items()}

    runs = group_files_by_run(files)

    all_pdf = DataFrame()
    frames = []
    data_list = []
    # NUM_CHANNELS=64
    # NUM_VIN=len(vin)
    for num, flist in runs.items():
        print('\n')
        print(f'{num=}')
        print(f'{flist=}')
        vin_amplitudes = defaultdict()
        vin_taus = defaultdict()

        for vin in flist:
            print(f'{vin=}')
            card_data = NWaveForm(data=vin[1], firmware='0x23040600')
            channels = card_data.data.shape[1]
            events = card_data.data.shape[0]

            amplitudes = np.zeros((events, channels))
            taus = np.zeros((events, channels))

            print(amplitudes.shape[0])
            print(amplitudes.shape[1])
            for event in range(events):
                print(f'{event=}')
                for channel in range(channels):
                    # print(f'{channel=}')
                    data_to_plot = card_data.data[event][channel]
                    try:# print(len(data_to_plot))
                        if PARITY == 'EVEN' and channel%2 == 0:
                            sampa = SampaFit(x=np.arange(len(data_to_plot)), y=data_to_plot)
                            amplitudes[event][channel] = sampa.amplitude
                            taus[event][channel] = sampa.tau

                        elif PARITY == 'ODD' and channel%2 == 1:
                            sampa = SampaFit(x=np.arange(len(data_to_plot)), y=data_to_plot)
                            amplitudes[event][channel] = sampa.amplitude
                            taus[event][channel] = sampa.tau
                        else:
                            amplitudes[event][channel] = 0
                            taus[event][channel] = 0
                    except Exception as e:
                        print(e)
                        amplitudes[event][channel] = 0
                        taus[event][channel] = 0
            # print(f'{amplitudes.mean(axis=0)=}')
            vin_amplitudes[f'{vin[0]}'] = amplitudes.mean(axis=0)
            vin_taus[f'{vin[0]}'] = taus.mean(axis=0)

        # print(vin_amplitudes)
        pdf_amplitudes = pd.DataFrame.from_dict(vin_amplitudes, orient='index')
        pdf_amplitudes.to_excel(Path(f'{RUNS_DIR}/{CARD_NUMBER}/{enc}/calculations/{num}-{CARD_NUMBER}-{enc}-amplitude.xlsx'))
        # print(f'{vin=}')
        pdf_taus = pd.DataFrame.from_dict(vin_taus, orient='index')
        pdf_taus.to_excel(Path(f'{RUNS_DIR}/{CARD_NUMBER}/{enc}/calculations/{num}-{CARD_NUMBER}-{enc}-tau.xlsx'))