from matplotlib import pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit
import numpy as np

from app.logic.data_structure.waveform import NWaveForm

np.set_printoptions(linewidth=1000, threshold=np.inf)

# filename = 'runs_old_to_11_09_24/454/raw/69-454.txt'
# filename = 'runs_old_to_11_09_24/385/raw/59-385.txt'
FILENAME2 = 'runs_old_to_11_09_24/454/0pF/raw/34-454.txt'
CHANNEL2 = 48
SAMPLE2 = 0

arr2 = NWaveForm(full_filename=FILENAME2)
y2 = arr2.waveform_data[SAMPLE2][CHANNEL2]
x2 = np.arange(len(y2))

# Создание новых данных для построения гладкой кривой сплайна
x_spline2 = np.linspace(0, len(y2) - 5, (len(y2) - 5) * 1000)
print(f'{len(x_spline2)=}')
# y_new = cs(x_spline)
spline2 = UnivariateSpline(x2, y2, k=5)

y_5_2 = spline2(x_spline2)
y_5_max_index2 = y_5_2.argmax()

FILENAME = '../../data/runs_old_to_11_09_24/454/0pF/raw/30-454.txt'
SAMPLE = 0
CHANNEL = 15
arr = NWaveForm(full_filename=FILENAME)
y = arr.waveform_data[SAMPLE][CHANNEL]
x = np.arange(len(y))
mean = y[:15].tau2()
sigma = y.std()
print(f'{mean=}')
print(f'{sigma=}')
max_value = y.max()
print(f'{max_value=}')

# y = [22.4155688819,22.3936180362,22.3177538001,22.1924849792,21.7721194577,21.1590235248,20.6670446864,20.4996957642,20.4260953411,20.3595072628,20.3926201626,20.6023149681,21.1694961343,22.1077417713,23.8270366414,26.5355924353,31.3179807276,42.7871637946,61.9639549412,84.7710953311]
# cs = CubicSpline(x, y)
spline = UnivariateSpline(x, y, k=5)

# Создание новых данных для построения гладкой кривой сплайна
x_spline = np.linspace(0, len(y) - 5, (len(y) - 5) * 1000)
print(f'{len(x_spline)=}')
# y_new = cs(x_spline)
y_5 = spline(x_spline)
y_5_max_index = y_5.argmax()


# Define a gaussian function with offset
def gaussian_func(x, a, x0, sigma, c):
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2)) + c




def half_gaussian(x, amplitude, mean, sigma, c):
    return amplitude * np.exp(-(x - mean) ** 2 / (2 * sigma ** 2)) * (x < mean) + c


initial_guess = [1024, 19.601, 0.2, mean]
popt, pcov = curve_fit(gaussian_func, x, y, p0=initial_guess)
print(f'{popt=}')
print(f'{pcov=}')
# plt.scatter(x, y)
x_gauss = np.linspace(0, len(y), len(y) * 1000)
y_gauss = gaussian_func(x_gauss, *popt)
y_gauss_max_index = y_gauss.argmax()


fig, ax = plt.subplots()
# plt.plot(x_gauss, y_gauss, label='Gaussian fit')
plt.plot(x, y, 'ob', label='Data ch15')
plt.plot(x_spline, y_5, 'b', label='Spline ch15')
plt.plot(x2, y2, 'or', label='Data ch48')
plt.plot(x_spline2, y_5_2, 'r', label='Spline ch48')

# plt.plot(x_new, y_new, 'g')
# text = "x={:.3f}, y={:.3f}".format(xmax, ymax)
#
# plt.annotate(text, xy=(xmax, ymax), xytext=(0.4, 0.9), **kw)
bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="b", lw=0.72)
bbox_props2 = dict(boxstyle="square,pad=0.3", fc="w", ec="r", lw=0.72)

arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60")
arrowprops2 = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=120")
kw = dict(xycoords='data', textcoords="axes fraction",
          arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
kw2 = dict(xycoords='data', textcoords="axes fraction",
           arrowprops=arrowprops2, bbox=bbox_props2, ha="right", va="top")
# ax.annotate(f'x={y_gauss_max_index / 1000}, y={y_gauss.max():.1f}', xy=(x_gauss[y_gauss_max_index], y_gauss.max()), xytext=(0.98, 0.9), **kw)
ax.annotate(f'x={y_5_max_index / 1000}, y={y_5.max():.1f}', xy=(x_spline[y_5_max_index], y_5.max()), xytext=(0.4, 0.9), **kw)
ax.annotate(f'x={y_5_max_index2 / 1000}, y={y_5_2.max():.1f}', xy=(x_spline2[y_5_max_index2], y_5_2.max()), xytext=(0.98, 0.9), **kw2)

ax.set_title(f'ch15 file=30, ch48 file=34')
ax.set_xlabel('time, sample (x100ns)')
ax.set_ylabel('ADC channel')





plt.legend(loc=(0.1, 0.2))
plt.show()
plt.close()

fig1, ax1 = plt.subplots()
# plt.plot(x, y, 'ob', label='Data ch15')
arr2.waveform_data
