import os
import re
import numpy as np
from matplotlib import pyplot as plt


class NWaveForm:
    def __init__(self, full_filename: str = None, raw_data: list[bytes] = None, event: int = -1):
        self.__event = event
        if full_filename:
            self.__full_filename = full_filename
            self.__raw_data = self.get_raw_data()
            self.__all_data = self.convert_data_to_int()
            self.__waveform_data = self.__all_data[:, :, 5:]
            self.__rms = self.get_rms()
        if raw_data:
            self.__full_filename = None
            self.__raw_data = np.array([[int(data, 16) for data in raw_data]],)
        self.__all_data = self.convert_data_to_int()
        self.__waveform_data = self.__all_data[:, :, 5:]
        self.__rms = self.get_rms()
        self.__max_value = self.get_max_value()

    @property
    def max_value(self):
        return self.__max_value

    @property
    def all_data(self):
        return self.__all_data

    @property
    def full_filename(self):
        return self.__full_filename

    @property
    def raw_data(self):
        return self.__raw_data

    @property
    def rms(self):
        return self.__rms

    @property
    def waveform_data(self):
        return self.__waveform_data

    def get_rms(self):
        self.__rms = self.__waveform_data.std(axis=(0, 2), ddof=1)
        return self.__rms

    def get_raw_data(self) -> np.ndarray:
        with open(self.__full_filename, 'r') as file:
            lines = file.readlines()
            print(f'{len(lines)=}')
        match self.__event:
            case -1:
                data_list = []
                for line in lines:
                    hex_values = line.strip().split()
                    decimal_values = [int(value, 16) for value in hex_values]
                    data_list.append(decimal_values)
                return np.array(data_list)

            case x if 0 <= x < len(lines):
                data_list = []
                hex_values = lines[x].strip().split()
                decimal_values = [int(value, 16) for value in hex_values]
                data_list.append(decimal_values)
                return np.array(data_list)
            case _:
                raise ValueError(f'{self.__event=} is not appropriate value')

    def check_data(self) -> bool:
        second_column = self.__all_data[:, :, 1]
        condition = second_column == 31
        return np.all(condition)

    def convert_data_to_int(self):
        # pass
        result_array_3d = np.zeros((self.__raw_data.shape[0],
                                    self.__raw_data.shape[1] // 12,
                                    self.__raw_data.shape[1] // 64 * 3), dtype=np.uint16)
        for i in range(result_array_3d.shape[0]):
            for j in range(result_array_3d.shape[1]):
                for k in range(result_array_3d.shape[2] // 3):
                    val = self.__raw_data[i, 12 * j + k]
                    d0 = val & 0x3ff
                    d1 = (val >> 10) & 0x3ff
                    d2 = (val >> 20) & 0x3ff
                    result_array_3d[i, j, 3 * k] = d0
                    result_array_3d[i, j, 3 * k + 1] = d1
                    result_array_3d[i, j, 3 * k + 2] = d2
        return result_array_3d

    def get_max_value(self):
        self.__max_value = self.__waveform_data.max(axis=(0, 2))
        return self.__max_value

    def plot_waveform(self):
        px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
        path = f'./plots/temp/'
        if not os.path.exists(path):
            os.makedirs(path)
        fig, axs = plt.subplots(8, 8, figsize=(3840 * px, 2160 * px), constrained_layout=True)
        fig.suptitle(f'WaveForm from file {self.__full_filename}')
        for row in range(8):
            for col in range(8):
                axs[row, col].plot(self.__waveform_data
                                   .transpose(1, 0, 2)
                                   .reshape(self.__waveform_data.shape[1], -1)[8 * row + col], 'o', )
                axs[row, col].set_ylim(0)
                axs[row, col].set_xlabel('time, sample (x100ns)')
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
        axs.set_title(f'RMS from file {self.__full_filename}')
        plt.show()
        # plt.savefig(f'{path}/34-454_rms_unconnected.png')


if __name__ == '__main__':
    np.set_printoptions(linewidth=1000, threshold=np.inf)

    filename = 'runs/454/10pF/raw/1-454.txt'
    a = NWaveForm(full_filename=filename, event=0)
    print(a.full_filename)
    print(a.raw_data.shape)

    print(a.all_data[0])
    print(a.check_data())
    print(a.get_rms())
    print(f'{a.get_max_value()=}')
    a.plot_waveform()
    a.plot_rms()

