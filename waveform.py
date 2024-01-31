import os
import re
import numpy as np
from matplotlib import pyplot as plt


class NWaveForm:
    def __init__(self, full_filename: str = None, raw_data: list[bytes] = None):
        if full_filename:
            separators = r'[/.-]'
            self.__full_filename = full_filename
            self.__filename = full_filename.split('/')[-1]
            parameters_list = re.split(separators, full_filename)
            self.__file_number = parameters_list[3]
            self.__card_number = parameters_list[4]
            self.__test_name = parameters_list[2]
            self.__raw_data = self.get_raw_data()
            # self.__all_data = self.convert_data_to_int()
            # self.__waveform_data = self.__all_data[:, :, 5:]
            # self.__rms = self.get_rms()
        if raw_data:
            # separators = r'[/.-]'
            self.__full_filename = None
            self.__filename = None
            # parameters_list = re.split(separators, full_filename)
            self.__file_number = None
            self.__card_number = None
            self.__test_name = None
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
    def filename(self):
        return self.__filename

    @property
    def card_number(self):
        return self.__card_number

    @property
    def test_name(self):
        return self.__test_name

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
        data_list = []
        for line in lines:
            hex_values = line.strip().split()
            decimal_values = [int(value, 16) for value in hex_values]
            data_list.append(decimal_values)
        return np.array(data_list)

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


# class WaveForm:
#     def __init__(self, raw_data: list[bytes],):
#         self.__rms = None
#         self.__raw_data = raw_data
#         self.__all_data = self.convert_data_to_int(raw_data)
#         self.__waveform_data = self.__all_data[:, 5:]
#
#     @property
#     def raw_data(self):
#         return self.__raw_data
#
#     @property
#     def all_data(self):
#         return self.__all_data
#
#     @property
#     def waveform_data(self):
#         return self.__waveform_data
#
#     @property
#     def rms(self):
#         return self.__rms
#
#     @staticmethod
#     def convert_data_to_int(raw_data: list[bytes]):
#         numpy_array = np.array([int(data, 16) for data in raw_data])
#         data = np.zeros((64, 3 * 12), dtype=np.uint16)
#         for j in range(64):
#             for k in range(12):
#                 val = numpy_array[12 * j + k]
#                 d0 = val & 0x3ff
#                 d1 = (val >> 10) & 0x3ff
#                 d2 = (val >> 20) & 0x3ff
#                 data[j, 3 * k] = d0
#                 data[j, 3 * k + 1] = d1
#                 data[j, 3 * k + 2] = d2
#         return data
#
#     def check_data(self):
#         second_column = self.__all_data[:, 1]
#         condition = second_column == 31
#         return np.all(condition)
#
#     def plot_waveform(self):
#         px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
#         path = f'./plots/temp/'
#         if not os.path.exists(path):
#             os.makedirs(path)
#         fig, axs = plt.subplots(8, 8, figsize=(3840 * px, 2160 * px), constrained_layout=True)
#         for row in range(8):
#             for col in range(8):
#                 axs[row, col].plot(self.__waveform_data[8 * row + col], 'o', )
#                 axs[row, col].set_ylim(0)
#                 axs[row, col].set_xlabel('time, us')
#                 axs[row, col].set_ylabel('ADC channel')
#                 axs[row, col].set_title(f'CH-{8 * row + col} WaveForm')
#         plt.show()
#         # plt.savefig(f'{path}/34-454_waveform_unconnected.png')
#
#     def plot_rms(self):
#         path = f'./plots/temp'
#         if not os.path.exists(path):
#             os.makedirs(path)
#         fig, axs = plt.subplots(1, constrained_layout=True)
#         axs.plot(self.__rms, 'o', )
#         axs.set_ylim(0)
#         axs.set_xlabel('Channel number')
#         axs.set_ylabel('RMS channel')
#         axs.set_title(f'RMS')
#         plt.show()
#         # plt.savefig(f'{path}/34-454_rms_unconnected.png')
#
#     def get_rms(self):
#         self.__rms = np.std(self.__waveform_data, axis=1, ddof=1)
#         return self.__rms


if __name__ == '__main__':
    np.set_printoptions(linewidth=1000, threshold=np.inf)

    filename = 'runs/385/raw/52-385.txt'
    a = NWaveForm(full_filename=filename)
    print(a.filename)
    print(a.card_number)
    print(a.full_filename)
    print(a.filename)
    print(a.test_name)
    print(a.raw_data.shape)

    print(a.all_data[0])
    print(a.check_data())
    print(a.get_rms())
    print(f'{a.get_max_value()=}')
    a.plot_waveform()
    a.plot_rms()

