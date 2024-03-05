import warnings

import numpy as np
from scipy.optimize import curve_fit, differential_evolution


class SampaFit():
    def __init__(self, x: np.ndarray, y: np.ndarray, t_sample: int = 1000):
        self.y = y
        self.x = x
        self.x_pulse = []
        self.y_pulse = []
        self.initial_guess_params = self.initial_guess()
        self.t_sample = t_sample
        self.bounds = ([self.initial_guess_params[0],
                        self.initial_guess_params[1] * 0.8,
                        self.initial_guess_params[2] * 0.995,
                        self.initial_guess_params[3]],
                       [self.initial_guess_params[0] * 1.5,
                        self.initial_guess_params[1] * 1.2,
                        self.initial_guess_params[2] * 1.1,
                        self.initial_guess_params[3] * 1.00001])

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
        baseline = self.y[:10].mean()
        # peaking time *tau 160ns but 100ns per sample
        tau = 1.6
        # start and end points
        threshold = baseline + 10 * self.y[:10].std()
        t_begin = np.where(self.y > threshold)[0][0]
        t_end = np.where(self.y[t_begin:] < threshold)[0][0] + t_begin

        self.x_pulse = self.x[t_begin - 3: t_end + 7]
        self.y_pulse = self.y[t_begin - 3: t_end + 7]
        self.y_pulse = np.where(self.y_pulse < threshold, baseline, self.y_pulse)

        #
        a = round((self.y_pulse.max() - baseline) * np.exp(4), 1)

        return a, t_begin, tau, baseline


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    from waveform import NWaveForm

    FILENAME = 'runs/454/0pF/raw/54-454.txt'
    CHANNEL = 26
    EVENT = 0
    arr2 = NWaveForm(full_filename=FILENAME)
    ampl = []
    px = 1 / plt.rcParams['figure.dpi']  # pixel in inches

    fig, ax = plt.subplots(figsize=(3840 * px, 2160 * px))

    for event in range(arr2.all_data.shape[0]):

        y = arr2.waveform_data[event][CHANNEL]
        x = np.arange(len(y))
        sampa = SampaFit(x, y)
        a, t, tau, baseline = sampa.diff_minimization()
        # ampl.append(round(a / np.exp(4), 1))

        popt, pcov = curve_fit(sampa.sampa_func, sampa.x_pulse, sampa.y_pulse,
                               p0=(a,t,tau,baseline))
        y2 = sampa.sampa_func(np.linspace(15,25,1000), *popt)
        ax.plot(np.linspace(15,25,1000), y2, 'b', label='Data ch15', ms=0.01)


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
