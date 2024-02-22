import sys
from PySide6 import QtWidgets
import matplotlib
from PySide6.QtWidgets import QWidget, QMainWindow
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import (
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from matplotlib.pyplot import subplots, plot

from waveform import NWaveForm

matplotlib.use("QtAgg")


class WaveformCanvas(FigureCanvasQTAgg):
    def __init__(self):
        # fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(8, 8)
        px = 1 / matplotlib.rcParams['figure.dpi']  # pixel in inches
        matplotlib.rcParams['axes.labelsize'] = 8
        matplotlib.rcParams['axes.titlesize'] = 8
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 8

        fig, axs = subplots(8, 8, figsize=(3840 * px, 2160 * px), constrained_layout=True)
        fig.suptitle('Waveform')
        for row in range(8):
            for col in range(8):
                axs[row][col].set_xlabel('time, sample (x100ns)')
                axs[row][col].set_ylabel('ADC channel')
                axs[row][col].set_title(f'CH-{8 * row + col}')
        super().__init__(fig)


class RMSCanvas(FigureCanvasQTAgg):
    def __init__(self):
        px = 1 / matplotlib.rcParams['figure.dpi']  # pixel in inches
        matplotlib.rcParams['axes.labelsize'] = 8
        matplotlib.rcParams['axes.titlesize'] = 8
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 8

        fig, axs = subplots(1, figsize=(800 * px, 600 * px), constrained_layout=True)
        fig.suptitle(f'RMS from file')

        # axs.plot(self.__rms, 'o', )
        # axs.set_ylim(0)
        axs.set_xlabel('Channel number')
        axs.set_ylabel('RMS channel')

        super().__init__(fig)


class WaveFormWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.waveform_canvas = WaveformCanvas()
        # Create toolbar, passing canvas as first parameter, parent(self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.waveform_canvas, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.waveform_canvas)
        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_plot(self, filename, event: int = -1):
        a = NWaveForm(full_filename=filename, event=event)
        self.waveform_canvas.figure.suptitle(f'WaveForm from {filename}')

        for row in range(64):
            self.waveform_canvas.figure.axes[row].cla()
            self.waveform_canvas.figure.axes[row].plot(a.waveform_data
                                                       .transpose(1, 0, 2)
                                                       .reshape(a.waveform_data.shape[1], -1)[row], 'o', ms=2)

            self.waveform_canvas.figure.axes[row].set_xlabel('time, sample (x100ns)')
            self.waveform_canvas.figure.axes[row].set_ylabel('ADC channel')
            self.waveform_canvas.figure.axes[row].set_title(f'CH-{row} WaveForm')
            self.waveform_canvas.figure.axes[row].set_ylim(0, a.max_value[row] * 1.2)

        self.waveform_canvas.draw()


class RMSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.rms_canvas = RMSCanvas()
        # Create toolbar, passing canvas as first parameter, parent(self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.rms_canvas, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.rms_canvas)
        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_plot(self, filename, event: int = -1):
        self.rms_canvas.figure.suptitle(f'RMS from {filename}')
        a = NWaveForm(full_filename=filename, event=event)

        for row in range(64):
            self.rms_canvas.figure.axes[0].cla()
            self.rms_canvas.figure.axes[0].set_ylim(0, a.rms.max()*1.2)
            self.rms_canvas.figure.axes[0].set_xlabel('Channel number')
            self.rms_canvas.figure.axes[0].set_ylabel('RMS channel')
            self.rms_canvas.figure.axes[0].plot(a.rms, 'o', )
        self.rms_canvas.draw()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # w = WaveFormWindow()
    w = RMSWindow()
    w.update_plot(filename='runs/385/4-385.txt')
    w.show()
    app.exec()
