import os
import re
from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from app.logic.sampa_fit import SampaFit
from app.config import RUNS_DIR

MaxCoords = namedtuple('MaxCoords', ['x', 'y'])
SplineParams = namedtuple('SplineParams', ['amplitude', 'max_val', 'baseline_10'])


@dataclass
class SplineData:
    x: np.ndarray
    y: np.ndarray
    max_coord: MaxCoords
    baseline_10: float
    amplitude: float


class NWaveFormOld:
    def __init__(self, full_filename: str = None, raw_data: list[bytes] = None, event: int = -1):
        self.__event = event
        if full_filename:
            self.__full_filename = full_filename
            self.__raw_data = self.get_raw_data()
            self.__raw_int_data = self.get_raw_int_data()
            # self.__all_data = self.convert_data_to_int()
            # self.__waveform_data = self.__all_data[:, :, 5:]
            # self.__rms = self.get_rms()
        if raw_data:
            self.__full_filename = None
            self.__raw_data = raw_data
            self.__raw_int_data = np.array([[int(data, 16) for data in self.__raw_data]], )
        self.__all_data = self.convert_data_to_int()
        self.__waveform_data = self.__all_data[:, :, 5:]
        self.__rms = self.get_rms()
        self.__max_value = self.get_max_value()
        self.n_events = self.__waveform_data.shape[0]

    @property
    def event(self):
        return self.__event

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
    def raw_int_data(self):
        return self.__raw_int_data

    @property
    def rms(self):
        return self.__rms

    @property
    def waveform_data(self):
        return self.__waveform_data

    def get_rms(self) -> np.array:
        self.__rms = self.__waveform_data.std(axis=(0, 2), ddof=1)
        return self.__rms

    def get_event_rms(self, event: int = 0) -> np.array:
        return self.__waveform_data[event, :, :].std(axis=1, ddof=1)

    def get_raw_data(self) -> np.ndarray:
        with open(self.__full_filename, 'r') as file:
            lines = file.readlines()
            print(f'{len(lines)=}')
        match self.__event:
            case -1:
                data_list = []
                for line in lines:
                    hex_values = line.strip().split()
                    # decimal_values = [int(value, 16) for value in hex_values]
                    data_list.append(hex_values)
                return np.array(data_list)

            case x if 0 <= x < len(lines):
                data_list = []
                hex_values = lines[x].strip().split()
                # decimal_values = [int(value, 16) for value in hex_values]
                data_list.append(hex_values)
                return np.array(data_list)
            case _:
                raise ValueError(f'{self.__event=} is not appropriate value')

    def get_raw_int_data(self) -> np.ndarray:
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
        result_array_3d = np.zeros((self.__raw_int_data.shape[0],
                                    self.__raw_int_data.shape[1] // 12,
                                    self.__raw_int_data.shape[1] // 64 * 3), dtype=np.uint16)
        for i in range(result_array_3d.shape[0]):
            for j in range(result_array_3d.shape[1]):
                for k in range(result_array_3d.shape[2] // 3):
                    val = self.__raw_int_data[i, 12 * j + k]
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

    def get_event_max_value(self, event: int = 0) -> int:
        self.__max_value = self.__waveform_data[event, :, :].max(axis=1)
        return self.__max_value

    def plot_waveform(self):
        px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
        path = f'../../../../temp/plots/temp/'
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

    def plot_fitted_waveform(self):
        px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
        path = f'../../../../temp/plots/temp/'
        if not os.path.exists(path):
            os.makedirs(path)
        fig, axs = plt.subplots(8, 8, figsize=(3840 * px, 2160 * px), constrained_layout=True)
        fig.suptitle(f'WaveForm from file {self.__full_filename} event {self.__event}')
        for row in range(8):
            for col in range(8):
                if self.__event == -1:
                    data_to_plot = self.__waveform_data.transpose(1, 0, 2).reshape(self.__waveform_data.shape[1], -1)[
                        8 * row + col]
                else:
                    data_to_plot = self.__waveform_data[0][8 * row + col]
                    sampa = SampaFit(x=np.arange(len(data_to_plot)), y=data_to_plot)
                    axs[row, col].plot(sampa.x_fit, sampa.y_fit, 'r', label='fit')
                    bbox = dict(boxstyle='square', facecolor='white', edgecolor='black', )
                    axs[row, col].annotate(f'Amplitude={sampa.amplitude:.1f}\n'
                                           f'Baseline={sampa.baseline:.1f}\n'
                                           f'Max={sampa.y_fit.max():.1f}\n'
                                           f't={sampa.t:.3f}\n'
                                           f'tau={sampa.tau:.3f}\n'
                                           f'a={sampa.a:.0f}\n',
                                           xy=(0.05, 0.3), xycoords='axes fraction',
                                           bbox=bbox)
                axs[row, col].plot(data_to_plot, 'o', )
                axs[row, col].set_ylim(0)
                axs[row, col].set_xlabel('time, sample (x100ns)')
                axs[row, col].set_ylabel('ADC channel')
                axs[row, col].set_title(f'CH-{8 * row + col} WaveForm')
        plt.show()
        # plt.savefig(f'{path}/34-454_waveform_unconnected.png')

    def make_fitted_amplitude_all_events(self):
        num_events = self.all_data.shape[0]
        num_channels = self.all_data.shape[1]
        amplitude = np.zeros((num_channels, num_events))

        for channel in range(num_channels):
            for event in range(num_events):
                # print(f'{self.__waveform_data[event]}')
                sampafit = SampaFit(x=np.arange(len(self.__waveform_data[event][channel])),
                                    y=self.__waveform_data[event][channel])
                # a,t,tau,bl = sampafit.diff_minimization()
                # amplitude[channel, event] = a/np.exp(4)

                amplitude[channel, event] = sampafit.amplitude
                # print(f'{amplitude[event, channel]=}')
        return amplitude

    def plot_fitted_amplitude(self):
        px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
        amplitude = self.make_fitted_amplitude_all_events()
        fig, axs = plt.subplots(8, 8, figsize=(3840 * px, 2160 * px), constrained_layout=True)
        fig.suptitle(f'Average amplitude from file {self.__full_filename}')
        for row in range(8):
            for col in range(8):
                channel = 8 * row + col
                y = amplitude[channel]
                axs[row, col].plot(y, 'ob', label='Data')

                axs[row, col].set_ylim(0, round(y.max()*1.1, -2))
                axs[row, col].set_xlabel('Events')
                axs[row, col].set_ylabel('ADC channel')
                axs[row, col].set_title(f'CH-{8 * row + col} Amplitudes')

                bbox = dict(boxstyle='square', facecolor='white', edgecolor='black', )
                axs[row, col].annotate(f'Std={y.std():.2f}\n'
                                       f'Mean={y.mean():.1f}\n'
                                       f'Max={y.max():.1f}\n'
                                       f'Min={y.min():.1f}',
                                       xy=(0.05, 0.1), xycoords='axes fraction',
                                       bbox=bbox)
        plt.show()

    # def make_spline(self, event, channel) -> SplineData:
    #     y = self.__waveform_data[event][channel]
    #     y_len = len(self.__waveform_data[event][channel])
    #     x = np.arange(y_len)
    #     spline = UnivariateSpline(x, y, k=5)
    #
    #     x_spline = np.linspace(15, y_len - 8, (y_len - 15 - 8) * 100 + 1)
    #     y_spline = spline(x_spline)
    #     y_max = y_spline[200:600].max()
    #     argmax = y_spline[200:600].argmax() + 200
    #     baseline_10 = y[0:10].mean()
    #     return SplineData(x=x_spline, y=y_spline, max_coord=MaxCoords(x_spline[argmax], y_max),
    #                       amplitude=y_max - baseline_10, baseline_10=baseline_10)

    # def make_spline_data_from_all_events(self):
    #     num_events = self.all_data.shape[0]
    #     num_channels = 64
    #     amplitude = np.zeros((num_channels, num_events))
    #     baseline_10 = np.zeros((num_channels, num_events))
    #     max_val = np.zeros((num_channels, num_events))
    #
    #     for channel in range(num_channels):
    #         for event in range(num_events):
    #             spline = self.make_spline(event, channel)
    #             amplitude[channel, event] = spline.amplitude
    #             baseline_10[channel, event] = spline.baseline_10
    #             max_val[channel, event] = spline.max_coord.y
    #             # print(f'{amplitude[event, channel]=}')
    #     return amplitude, baseline_10, max_val

    # def plot_spline_data(self):
    #     px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
    #     amplitude, baseline_10, max_val = self.make_spline_data_from_all_events()
    #     fig, axs = plt.subplots(8, 8, figsize=(3840 * px, 2160 * px), constrained_layout=True)
    #     fig.suptitle(f'Average amplitude from file {self.__full_filename}')
    #     for row in range(8):
    #         for col in range(8):
    #             channel = 8 * row + col
    #             y = amplitude[channel]
    #             axs[row, col].plot(y, 'ob', label='Data')
    #
    #             axs[row, col].set_ylim(0)
    #             axs[row, col].set_xlabel('Events')
    #             axs[row, col].set_ylabel('ADC channel')
    #             axs[row, col].set_title(f'CH-{8 * row + col} Amplitudes')
    #
    #             bbox = dict(boxstyle='square', facecolor='white', edgecolor='black', )
    #             axs[row, col].annotate(f'Mean={y.mean():.1f}\n'
    #                                    f'Max={y.max():.1f}\n'
    #                                    f'Min={y.min():.1f}',
    #                                    xy=(0.05, 0.1), xycoords='axes fraction',
    #                                    bbox=bbox)

    # def plot_waveform_with_spline(self, event):
    #     px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
    #     path = f'./plots/temp/'
    #     if not os.path.exists(path):
    #         os.makedirs(path)
    #     fig, axs = plt.subplots(8, 8, figsize=(3840 * px, 2160 * px), constrained_layout=True)
    #     fig.suptitle(f'WaveForm of event {event} from file {self.__full_filename}')
    #     for row in range(8):
    #         for col in range(8):
    #             channel = 8 * row + col
    #             y = self.__waveform_data[event][channel]
    #             spline_data = self.make_spline(event=event, channel=channel)
    #
    #             axs[row, col].plot(y, 'ob', label='Data')
    #             axs[row, col].plot(spline_data.x, spline_data.y, color='r', label='Spline')
    #
    #             axs[row, col].set_ylim(0)
    #             axs[row, col].set_xlabel('time, sample (x100ns)')
    #             axs[row, col].set_ylabel('ADC channel')
    #             axs[row, col].set_title(f'CH-{8 * row + col} WaveForm')
    #             bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="b", lw=0.72)
    #             arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60")
    #             kw = dict(xycoords='data', textcoords="axes fraction",
    #                       arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    #             axs[row, col].annotate(f'x={spline_data.max_coord.x:.2f}, y={spline_data.max_coord.y:.1f}',
    #                                    xy=(spline_data.max_coord.x, spline_data.max_coord.y),
    #                                    xytext=(0.4, 0.9), **kw)
    #
    #             bbox = dict(boxstyle='square', facecolor='white', edgecolor='black', )
    #             axs[row, col].annotate(f'Amplitude={spline_data.amplitude:.1f}\n'
    #                                    f'Baseline={spline_data.baseline_10:.1f}',
    #                                    xy=(0.05, 0.1), xycoords='axes fraction',
    #                                    bbox=bbox)

        plt.show()

    def plot_rms(self):
        path = f'../../../../temp/plots/temp'
        if not os.path.exists(path):
            os.makedirs(path)
        rms_mean = np.full(len(self.__rms), self.__rms.mean())
        fig, axs = plt.subplots(1, constrained_layout=True)
        axs.plot(self.__rms, 'o', )
        axs.plot(rms_mean, 'r')
        axs.set_ylim(0)
        axs.set_xlabel('Channel number')
        axs.set_ylabel('RMS channel')
        axs.set_title(f'RMS from file {self.__full_filename}')
        bbox = dict(boxstyle='square', facecolor='white', edgecolor='black', )
        axs.annotate(f'RMS Mean={rms_mean[0]:.3f}',
                     xy=(0.05, 0.1), xycoords='axes fraction',
                     bbox=bbox)
        plt.show()
        # plt.savefig(f'{path}/34-454_rms_unconnected.png')


def linearity_df(card_num, cdet, test):

    paths = Path(f'runs/{card_num}/{cdet}pF/{test}/').glob('*.txt')
    print(paths)
    # for i in paths:
    #     print(f'{i=}')
    vin = sorted([float(re.search(r'\d\.\d+', str(i))[0]) for i in paths])
    print(f'{vin=}')
    frames = []
    for idx in vin:
        data_list = []
        filename = f'runs/{card_num}/{cdet}pF/{test}/1-{card_num}-even-2pF-{idx}V.txt'
        print(f'{filename=}')
        card_data = NWaveFormOld(full_filename=filename, event=-1)
        for event in range(0, card_data.n_events):
            for row in range(8):
                for col in range(8):
                    channel = 8 * row + col
                    data_to_plot = card_data.waveform_data[event][channel]
                    # print(f'{event=}, {channel=}')
                    sampa = SampaFit(x=np.arange(len(data_to_plot)), y=data_to_plot)
                    dataset = [event, channel, sampa.amplitude, sampa.baseline, sampa.tau]
                    data_list.append(dataset)
        columns = ['event', 'channel', 'amplitude', 'baseline', 'tau']
        df = pd.DataFrame(data_list, columns=columns)
        df.set_index(['event', 'channel'], inplace=True)
        mean_df = df.groupby('channel').mean()
        mean_df['vin'] = idx
        # print(f'{idx=}<<>>{mean_df.to_string()=}')
        # print(f'{mean_df.to_string()}')
        frames.append(mean_df.reset_index())

    df2 = pd.concat(frames)
    # df2['index_in_channel'] = df2.groupby('channel').cumcount()
    df2.set_index(['vin', 'channel', ], inplace=True)
    return df2

if __name__ == '__main__':
    np.set_printoptions(linewidth=1000, threshold=np.inf)


    card_num = 345
    cdet = 0
    test = 'gain'
    filename = f'{RUNS_DIR}/{card_num}/{cdet}pF/{test}/1-345-even-2pF-0.05V.txt'
    paths = Path(f'{RUNS_DIR}/{card_num}/{cdet}pF/{test}/').glob('*.txt')
    print(paths)
    # for i in paths:
    #     print(f'{i=}')
    vin = sorted([float(re.search(r'\d\.\d+', str(i))[0]) for i in paths])
    print(f'{vin=}')

    # breakpoint()

    # print(a.full_filename)
    # print(a.all_data.shape[0])
    # idx = 0
    # for ch in a.all_data[3]:
    #     print(f'ch{idx}={ch}')
    #     idx += 1
    # a.plot_fitted_waveform()
    a = NWaveFormOld(full_filename=filename, event=0)

    # print(a.waveform_data)
    print(a.raw_data)
    print(f'{a.raw_int_data}')
    print(len(a.raw_int_data[0]))
    # for i in a.raw_int_data[0]:
    #     print(f'{i} <-> d0={(i & 0x3ff)} d1={(i>>10) & 0x3ff} d2={(i>>20) & 0x3ff}', end='\n')
    # print(a.check_data())
    # print(f'{a.get_rms()=}')
    # print(f'{a.get_event_rms(0)=}')
    # print(f'{a.get_max_value()=}')
    # print(f'{a.get_event_max_value(0)=}')

    # a.plot_waveform()
    # a.plot_waveform_with_spline(0)

    # a.plot_fitted_waveform()###########################################################
    # a.plot_fitted_amplitude()
    #
    # a.plot_rms()
    # df2_10 = linearity_df('345', '10', 'gain')
    # df2_20 = linearity_df('345', '20', 'gain')
    # df2_40 = linearity_df('345', '40', 'gain')
    #
    # amplitudes_channel_10 = df2_10.loc[(slice(None), 0), 'amplitude']
    # amplitudes_channel_10 = amplitudes_channel_10.reset_index(level='channel', drop=True)
    #
    # amplitudes_channel_20 = df2_20.loc[(slice(None), 0), 'amplitude']
    # amplitudes_channel_20 = amplitudes_channel_20.reset_index(level='channel', drop=True)
    #
    # amplitudes_channel_40 = df2_40.loc[(slice(None), 0), 'amplitude']
    # amplitudes_channel_40 = amplitudes_channel_40.reset_index(level='channel', drop=True)
    #
    # plt.figure(figsize=(10, 6))
    # plt.plot(amplitudes_channel_10.index[0:-1], amplitudes_channel_10.values[0:-1], marker='o', color='blue')
    # plt.plot(amplitudes_channel_20.index[0:-1], amplitudes_channel_20.values[0:-1], marker='o', color='red')
    # plt.plot(amplitudes_channel_40.index[0:-1], amplitudes_channel_40.values[0:-1], marker='o', color='green')
    #
    # plt.title('Зависимость амплитуд от mini_df_index для канала 0')
    # plt.xlabel('mini_df_index')
    # plt.ylabel('amplitude')
    # plt.grid(True)
    # plt.show()
    #
    #
    # # breakpoint()
    # # fig, axs = plt.subplots(1, constrained_layout=True)
    # # axs.plot(mean_df['amplitude'], 'o', )
    # # # axs.plot(rms_mean, 'r')
    # # axs.set_ylim(0)
    # # axs.set_xlabel('Channel number')
    # # axs.set_ylabel('RMS channel')
    # # axs.set_title(f'RMS from file {filename}')
    # # bbox = dict(boxstyle='square', facecolor='white', edgecolor='black', )
    # # # axs.annotate(f'RMS Mean={rms_mean[0]:.3f}',
    # # #              xy=(0.05, 0.1), xycoords='axes fraction',
    # # #              bbox=bbox)
    # # plt.show()
