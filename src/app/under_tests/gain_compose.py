"""
собираем данные в 1 файл.
создается 2 файла:
    1) линейность
    2) данные события в LSB
"""


from pathlib import Path
import re

import numpy as np
from pandas import DataFrame

from app.logic.sampa_fit import SampaFit
from app.logic.data_structure.waveform import NWaveForm

paths = Path(f'../../../data/gain/').glob('*.txt')
print(paths)
# for i in paths:
#     print(f'{i=}')


vin = sorted([float(re.search(r'\d\.\d+', str(i))[0]) for i in paths])
print(f'{len(vin)=}')
frames = []
data_list = []
for i in range(0,0):
    print('hello')


for idx in vin:
    filename = f'gain/1-317-odd-2pF-{idx}V.txt'
    print(f'{filename=}')
    event = 0
    card_data = NWaveForm(full_filename=filename, event=event)
    # for event in range(0, card_data.n_events):
    # for row in range(8):
    #     for col in range(8):
    #         channel = 8 * row + col
    data_to_plot = card_data.waveform_data[event][7]
    # print(f'{event=}, {7}, {data_to_plot=}')
    frames.append(data_to_plot)
    sampa = SampaFit(x=np.arange(len(data_to_plot)), y=data_to_plot)
    dataset = sampa.amplitude
    data_list.append(dataset)
df = DataFrame(frames)
df_linearity = DataFrame(data_list)
df.index = vin
print(df)
df_linearity.index = vin
print(df_linearity)
df.to_csv('gain/1-317-odd-2pF-all.csv')
df_linearity.to_csv('gain/linearity.csv')
print(f'{vin=}')