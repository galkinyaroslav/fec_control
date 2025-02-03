from collections import namedtuple

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

file_list = [f'{i}_VAT' for i in range(31)]
header = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0', 'Tsam', 'Va2_1_25',
          'mA3_S1',
          'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']
VAT = namedtuple('VAT', header)


def make_tuple_data(file):
    with open(f'narrowpart/{file}') as f:
        lines = f.readlines()
        data = [float(val) for val in lines[2].strip().split(' ') if val != '']
        return VAT._make(data)


roc_vat = [make_tuple_data(file) for file in file_list]
temperature = [roc_vat[link].T for link in range(31)]
s_temperature = [roc_vat[link].Tsam for link in range(31)]
print(temperature)

# fig, axs = plt.subplots(2, constrained_layout=True)
#
# axs[0].plot(range(31), temperature, 'o', )
# axs[1].plot(range(31), s_temperature, 'o', )
# # axs[0].plot(values_pdf, 'o', )
# # axs[1].plot(rms_pdf, 'o', )
# axs[0].set_ylim(0)
# axs[1].set_ylim(0)
#
# # axs[0].legend(list(values), loc='center left', bbox_to_anchor=(0.96, 0.5))
# axs[0].set_xlabel('link')
# axs[0].set_ylabel('Temperature, °C')
# axs[1].set_xlabel('link')
# axs[1].set_ylabel('Temperature, °C')
# # axs[1].set_xlabel('time, us')
# # axs[1].set_ylabel('ADC channel')
# axs[0].set_title(f'T')
# axs[1].set_title(f'Tsam')
plt.plot(range(31), temperature, 'o', )
plt.plot(range(31), s_temperature, 'o', )
plt.ylim(0, 35)
plt.xlabel('Link number')
plt.ylabel('Temperature, °C')
plt.title('Temperatures for each link')
plt.legend(['T', 'Tsam'], loc='center left', bbox_to_anchor=(1.04, 0.5),borderaxespad=0)
plt.tight_layout()

plt.show()
