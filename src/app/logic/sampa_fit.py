import warnings
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit, differential_evolution

from app.config import DATA_DIR, RUNS_DIR


class SampaFit():
    def __init__(self, x: np.ndarray, y: np.ndarray, t_sample: int = 1000):
        self.y = y
        self.x = x
        self.x_pulse = []
        self.y_pulse = []
        self.initial_guess_params = self.initial_guess()
        self.t_sample = t_sample
        self.bounds = ([self.initial_guess_params[0]*0.9,
                        self.initial_guess_params[1] * 0.9,
                        self.initial_guess_params[2] ,
                        self.initial_guess_params[3]*0.95],
                       [self.initial_guess_params[0] * 1.5,
                        self.initial_guess_params[1] * 1.2,
                        self.initial_guess_params[2] * 1.2,
                        self.initial_guess_params[3] * 1.05])
        # if self.initial_guess_params == (0,0,0,0):
        #     self.a, self.t, self.tau, self.baseline = self.initial_guess_params
        #     self.x_fit = [0]
        #
        #     self.y_fit = [0]
        #     self.amplitude = 0
        # else:
        self.a, self.t, self.tau, self.baseline = self.get_fit_params()
        self.x_fit = np.linspace(self.x_pulse[0], self.x_pulse[-1], len(self.x) * self.t_sample + 1)

        self.y_fit = self.sampa_func(self.x_fit, self.a, self.t, self.tau, self.baseline)
        self.amplitude = self.y_fit.max() - self.baseline

    def sumOfSquaredError(self, parameterTuple):
        warnings.filterwarnings("ignore")  # do not print warnings by genetic algorithm
        return np.sum((self.y_pulse - self.sampa_func(self.x_pulse, *parameterTuple)) ** 2)

    def diff_minimization(self):
        bounds = ((self.initial_guess_params[0], self.initial_guess_params[0] * 1.6),
                  (self.initial_guess_params[1] * 0.8, self.initial_guess_params[1] * 1.2),
                  (self.initial_guess_params[2] , self.initial_guess_params[2] * 1.5),
                  (self.initial_guess_params[3], self.initial_guess_params[3]))

        result = differential_evolution(self.sumOfSquaredError, bounds, seed=3)
        return result.x

    def get_fit_params(self):
        popt, pcov = curve_fit(self.sampa_func, self.x_pulse, self.y_pulse,
                               p0=self.initial_guess_params,
                               bounds=self.bounds)
        return popt

    def sampa_func(self, x, a, t, tau, baseline):
        n = 4
        y_full = a * (((x - t) / tau) ** n) * np.exp(-n * ((x - t) / tau)) + baseline
        y_full = np.where(x < t, baseline, y_full)
        return y_full

    def initial_guess(self):
        # initial baseline
        baseline = self.y[:14].mean()
        # peaking time *tau 160ns but 100ns per sample
        tau = 1.6
        # start and end points
        try:
            atd = self.y[:14].std()
            # print(f'{atd=}')
            threshold = baseline + 3 * atd
            # print(f'{self.y=}')
            # op = np.where(self.y > threshold)[0]
            t_begin = self.y.argmax()-1 if self.y.argmax()-2<threshold else self.y.argmax()-2
            # self.y.argmax()

            # if len(op) >= 4:
            #     result = None
            #
            #     for i in range(len(op)-2):
            #         if abs(op[i] - op[i + 1]) == 1 and abs(op[i + 1] - op[i + 2]) == 1:  # проверяем разницу
            #             result = i
            #             break
            #     t_begin = op[result]
            # elif len(op) >= 3:
            #     t_begin = self.y.argmax()-1
            # else:
            #     t_begin = op[0]


            # print(f'{op=}')
            # print(f'{threshold=}')
            # print(f'{t_begin=}')
        except IndexError as e:
            threshold = baseline + 4 * self.y[:10].std()
            print(f'{e=}')
            t_begin = np.where(self.y > threshold)[0][0]
        try:
            t_end = np.where(self.y[t_begin+1:] < 1.1*threshold)[0][0]+t_begin+1
        except IndexError as e:
            t_end = t_begin+10
            print(e)
        # print(f'{t_begin=}, {t_end=}, {threshold=}')
        # print()
        self.x_pulse = self.x[t_begin - 3: t_end + 7]
        self.y_pulse = self.y[t_begin - 3: t_end + 7]

        self.y_pulse = np.where(self.y_pulse < threshold, baseline, self.y_pulse)
        # if len(self.y_pulse)==0:
        #     return (0,0,0,0)
        # else:
        a = round((self.y_pulse.max() - baseline) * np.exp(4), 1)

        return a, t_begin, tau, baseline


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    from app.logic.data_structure.factory import NWaveForm

    FILENAME = Path(DATA_DIR,'runs_old_to_11_09_24','454/0pF/raw/54-454.txt')
    FILENAME = Path(RUNS_DIR,'1181/0pF/gain/3-1181-even-2pF-0.6V.txt')

    CHANNEL = 1
    EVENT = 5
    firmware = ['0x23040400', '0x23040600', '0x24040800', ]
    arr2 = NWaveForm(data=FILENAME, firmware=firmware[2])
    ampl = []
    px = 1 / plt.rcParams['figure.dpi']  # pixel in inches

    fig, ax = plt.subplots()

    for event in range(arr2.data.shape[0]):

        y = arr2.data[EVENT][CHANNEL]
        x = np.arange(len(y))
        sampa = SampaFit(x, y)
        # a, t, tau, baseline = sampa.diff_minimization()
        # print(a, t, tau, baseline)
        # ampl.append(round(a / np.exp(4), 1))

        # popt, pcov = curve_fit(sampa.sampa_func, sampa.x_pulse, sampa.y_pulse,
        #                        p0=(a,t,tau,baseline))
        popt = [sampa.a, sampa.t, sampa.tau, sampa.baseline]
        # sampa.get_fit_params()
        # print(sampa.initial_guess_params)
        # print(popt)
        y2 = sampa.sampa_func(np.linspace(0,30,1000), *popt)
        ax.plot(np.linspace(0,30,1000), y2, f'r', label="Fitting SampaFunc", ms=0.01)
        plt.xlabel("Sample x 100, ns")  # подпись оси X
        plt.ylabel("ADC, count")  # подпись оси Y
        plt.title("Sampa function fitting")  # название графика
        ax.plot(x, y, 'bo', label="Initial data")
        plt.legend(loc="upper left",framealpha=0)
        # ax.plot(arr2.data[event][CHANNEL], 'b', label='Data ch15', ms=0.01)
        break

    # ax.set_xlabel('time, sample (x100ns)')
    # ax.set_ylabel('ADC channel')
    # ax.set_title(f'WaveForm of CH-{CHANNEL} event-{EVENT} from file {FILENAME}')
    #
    #
    # ax.plot(sampa.x_fit, sampa.y_fit, 'r', label='1')
    # bbox = dict(boxstyle='square', facecolor='white', edgecolor='black', )
    # ax.annotate(f'Amplitude={sampa.amplitude:.1f}\n'
    #             f'Baseline={sampa.baseline:.1f}\n'
    #             f'Max={sampa.y_fit.max():.1f}\n'
    #             f't={sampa.t:.3f}\n'
    #             f'tau={sampa.tau:.3f}\n'
    #             f'a={sampa.a:.0f}\n',
    #             xy=(0.73, 0.65), xycoords='axes fraction',
    #             bbox=bbox)
    plt.show()

