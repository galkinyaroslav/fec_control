import os

import numpy as np
from matplotlib import pyplot as plt


# class NWaveForm:
#     def __init__(self, filename: str):
#         self.__rms = None
#         self.__raw_data = raw_data
#         self.__all_data = self.convert_data_to_int(raw_data)
#         self.__waveform_data = self.__all_data[:, 5:]
#
#     def asd(self):
#         filename = 'events.lst'
#         with open(f'{filename}', 'r') as file:
#             lines = file.readlines()
#         decimal_values = []
#         for line in lines:
#             line = line.strip().split()
#             decimal_values = ([value.lstrip('0x').encode() for value in line])
#         print(decimal_values)

class WaveForm:
    def __init__(self, raw_data: list[bytes],):
        self.__rms = None
        self.__raw_data = raw_data
        self.__all_data = self.convert_data_to_int(raw_data)
        self.__waveform_data = self.__all_data[:, 5:]

    @property
    def raw_data(self):
        return self.__raw_data

    @property
    def all_data(self):
        return self.__all_data

    @property
    def waveform_data(self):
        return self.__waveform_data

    @property
    def rms(self):
        return self.__rms

    @staticmethod
    def convert_data_to_int(raw_data: list[bytes]):
        numpy_array = np.array([int(data, 16) for data in raw_data])
        data = np.zeros((64, 3 * 12), dtype=np.uint16)
        for j in range(64):
            for k in range(12):
                val = numpy_array[12 * j + k]
                d0 = val & 0x3ff
                d1 = (val >> 10) & 0x3ff
                d2 = (val >> 20) & 0x3ff
                data[j, 3 * k] = d0
                data[j, 3 * k + 1] = d1
                data[j, 3 * k + 2] = d2
        return data

    def check_data(self):
        second_column = self.__all_data[:, 1]
        condition = second_column == 31
        return np.all(condition)

    def plot_waveform(self):
        px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
        path = f'./plots/temp/'
        if not os.path.exists(path):
            os.makedirs(path)
        fig, axs = plt.subplots(8, 8, figsize=(3840 * px, 2160 * px), constrained_layout=True)
        for row in range(8):
            for col in range(8):
                axs[row, col].plot(self.__waveform_data[8 * row + col], 'o', )
                axs[row, col].set_ylim(0)
                axs[row, col].set_xlabel('time, us')
                axs[row, col].set_ylabel('ADC channel')
                axs[row, col].set_title(f'CH-{8 * row + col} WaveForm')
        plt.show()
        # plt.savefig(f'{path}/34-454_waveform_unconnected.png')

    def plot_rms(self):
        path = f'./plots/temp'
        if not os.path.exists(path):
            os.makedirs(path)
        fig, axs = plt.subplots(1, constrained_layout=True)
        axs.plot(self.__rms, 'o', )
        axs.set_ylim(0)
        axs.set_xlabel('Channel number')
        axs.set_ylabel('RMS channel')
        axs.set_title(f'RMS')
        plt.show()
        # plt.savefig(f'{path}/34-454_rms_unconnected.png')

    def get_rms(self):
        self.__rms = np.std(self.__waveform_data, axis=1, ddof=1)
        return self.__rms

# np.set_printoptions(linewidth=1000, threshold=np.inf)

# def get_waveform_data():
#     result_array_3d = result_array_3d[:, :, 5:]


def test():
    filename = 'events.lst'
    with open(f'{filename}', 'r') as file:
        lines = file.readlines()
    decimal_values = []
    for line in lines:
        line = line.strip().split()
        decimal_values = ([value.lstrip('0x').encode() for value in line])
    print(decimal_values)
    # np.set_printoptions(linewidth=1000, threshold=np.inf)


if __name__ == '__main__':
    np.set_printoptions(linewidth=1000, threshold=np.inf)

    filename = 'runs/454/raw/43-454.txt'
    with open(f'{filename}', 'r') as file:
        lines = file.readlines()
    decimal_values = ([value.lstrip('0x').encode() for value in lines[0].strip().split()])
    # for line in lines:
    #     line = line.strip().split()
    #     decimal_values = ([value.lstrip('0x').encode() for value in line])
    print(decimal_values)
    a = WaveForm(decimal_values)
    b = a.all_data
    c = a.raw_data
    d = a.waveform_data
    print(f'{b=}')
    print(len(b))
    print(f'{c=}')
    print(len(c))

    print(f'{d=}')
    print(len(d[0]))
    print('checked: ', a.check_data())
    a.get_rms()
    a.plot_waveform()
    a.plot_rms()
