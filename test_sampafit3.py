import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from waveform import NWaveForm





def initial_guess(x: np.array, y: np.array) -> np.array:
    ''' x begins from 0!!!'''

    # initial baseline
    baseline = y[:10].mean()
    # peaking time *tau 160ns but 100ns per sample
    tau = 1.6

    # start and end points
    threshold = baseline + 3 * y[:10].std()
    t_begin = np.where(y > threshold)[0][0]
    t_end = np.where(y[t_begin:] < threshold)[0][0] + t_begin

    # x_pulse = x[t_begin - 3: t_end + 7]
    y_pulse = y[t_begin - 3: t_end + 7]

    #
    a = round((y_pulse.max() - baseline) * np.exp(4), 1)

    return a, t_begin, tau, baseline, t_end, threshold


FILENAME = 'runs/454/0pF/raw/54-454.txt'
CHANNEL = 48
EVENT = 99

arr2 = NWaveForm(full_filename=FILENAME)
y = arr2.waveform_data[EVENT][CHANNEL]
x = np.arange(len(y))

a, t_begin, tau, baseline, t_end, threshold = initial_guess(x, y)
print(a, t_begin, tau, baseline, t_end, threshold)
initial_guess_params = a, t_begin, tau, baseline
# initial_guess_params = a, t_begin, tau

print("Initial Guess Parameters:", initial_guess_params)

def sampa_fit2(x, a, t, tau, baseline):
    n = 4
    # t = 0
    y_full = a * (((x - t) / tau) ** n) * np.exp(-n * ((x - t) / tau)) + baseline

    # y_full[:np.argmax(x[x < math.floor(t)])] = baseline
    y_full = np.where(x < t, baseline, y_full)

    return y_full




x_pulse = x[t_begin - 3: t_end + 7]
y_pulse = y[t_begin - 3: t_end + 7]
y_pulse = np.where(y_pulse < threshold, baseline, y_pulse)
print(y_pulse)

t_sample = 100
x_fit = np.linspace(x_pulse[0], x_pulse[-1], len(x) * t_sample + 1)
y_fit = sampa_fit2(x=x_fit, a=a, t=t_begin, tau=tau, baseline=baseline)
# y_fit = sampa_fit2(x=x_fit, a=a, t=t_begin, tau=tau)

# print(x_fit)
bounds = ([initial_guess_params[0] * 0.99, initial_guess_params[1] * 0.95, initial_guess_params[2] * 0.95,
           initial_guess_params[3] *0.99999],
          [initial_guess_params[0] * 1.5, initial_guess_params[1] * 1.1, initial_guess_params[2] * 1.1,
           initial_guess_params[3] *1.00001])

popt, pcov = curve_fit(sampa_fit2, x_pulse, y_pulse,
                       p0=initial_guess_params,
                       bounds=bounds)
# err = np.sqrt(np.diag(pcov))
#
# print(f'{popt=}')
# print(f'{pcov=}')
# print(f'{err=}')
y_curve_fit = sampa_fit2(x_fit, *popt)

fig, ax = plt.subplots()
ax.set_xlabel('time, sample (x100ns)')
ax.set_ylabel('ADC channel')
ax.set_title(f'WaveForm of CH-{CHANNEL} event-{EVENT} from file {FILENAME}')

ax.plot(x, y, 'ob', label='Data ch15')

ax.plot(x_fit, y_curve_fit, 'r', label='1')
bbox = dict(boxstyle='square', facecolor='white', edgecolor='black', )
ax.annotate(f'Amplitude={y_curve_fit.max() - baseline:.1f}\n'
            f'Baseline={baseline:.1f}\n'
            f'Max={y_curve_fit.max():.1f}\n'
            f't={popt[1]:.3f}\n'
            f'tau={popt[2]:.3f}\n'
            f'a={popt[0]:.0f}\n',
            xy=(0.73, 0.65), xycoords='axes fraction',
            bbox=bbox)
plt.show()
