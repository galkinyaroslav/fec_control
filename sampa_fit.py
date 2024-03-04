import numpy as np
from scipy.optimize import curve_fit



class SampaFit():
    def __init__(self, x: np.ndarray, y: np.ndarray, t_sample: int = 100):
        self.y = y
        self.x = x
        self.x_pulse = []
        self.y_pulse = []
        self.initial_guess_params = self.initial_guess()
        self.t_sample = t_sample
        self.bounds = ([self.initial_guess_params[0] * 0.99,
                        self.initial_guess_params[1] * 0.8,
                        self.initial_guess_params[2] * 0.995,
                        self.initial_guess_params[3] * 0.99999],
                       [self.initial_guess_params[0] * 1.5,
                        self.initial_guess_params[1] * 1.2,
                        self.initial_guess_params[2] * 1.005,
                        self.initial_guess_params[3] * 1.00001])

        self.a, self.t, self.tau, self.baseline = self.get_fit_params()
        self.x_fit = np.linspace(self.x_pulse[0], self.x_pulse[-1], len(self.x) * self.t_sample + 1)

        self.y_fit = self.sampa_func(self.x_fit, self.a, self.t, self.tau, self.baseline)
        self.amplitude = self.y_fit.max() - self.baseline


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
        threshold = baseline + 6 * self.y[:10].std()
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
    CHANNEL = 48
    EVENT = 0
    arr2 = NWaveForm(full_filename=FILENAME)
    y = arr2.waveform_data[EVENT][CHANNEL]
    x = np.arange(len(y))
    sampa = SampaFit(x, y)

    fig, ax = plt.subplots()
    ax.set_xlabel('time, sample (x100ns)')
    ax.set_ylabel('ADC channel')
    ax.set_title(f'WaveForm of CH-{CHANNEL} event-{EVENT} from file {FILENAME}')

    ax.plot(x, y, 'ob', label='Data ch15')

    ax.plot(sampa.x_fit, sampa.y_fit, 'r', label='1')
    bbox = dict(boxstyle='square', facecolor='white', edgecolor='black', )
    ax.annotate(f'Amplitude={sampa.amplitude:.1f}\n'
                f'Baseline={sampa.baseline:.1f}\n'
                f'Max={sampa.y_fit.max():.1f}\n'
                f't={sampa.t:.3f}\n'
                f'tau={sampa.tau:.3f}\n'
                f'a={sampa.a:.0f}\n',
                xy=(0.73, 0.65), xycoords='axes fraction',
                bbox=bbox)
    plt.show()
