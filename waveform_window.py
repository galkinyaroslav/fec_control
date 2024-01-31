import sys
from PySide6 import QtWidgets
import matplotlib
from PySide6.QtWidgets import QWidget, QMainWindow
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import (
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from matplotlib.pyplot import subplots

from waveform import NWaveForm

matplotlib.use("QtAgg")


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(8, 8)
        px = 1 / matplotlib.rcParams['figure.dpi']  # pixel in inches
        matplotlib.rcParams['axes.labelsize'] = 8
        matplotlib.rcParams['axes.titlesize'] = 8
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 8

        fig, axs = subplots(8, 8, figsize=(1920 * px, 1080 * px), constrained_layout=True)
        fig.suptitle("Waveform")
        for row in range(8):
            for col in range(8):
                axs[row][col].set_xlabel('time, sample (x100ns)')
                axs[row][col].set_ylabel('ADC channel')
                axs[row][col].set_title(f'CH-{8 * row + col} WaveForm')
        super().__init__(fig)


class WaveFormWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.waveform_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.figure.axes[1].set_title('wave2')

        # sc.axes[1].plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        # Create toolbar, passing canvas as first parameter, parent(self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.waveform_canvas, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.waveform_canvas)
        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_plot(self, filename):
        for row in range(64):
            a = NWaveForm(full_filename=filename)

            self.waveform_canvas.figure.suptitle(f'WaveForm from {filename}')
            self.waveform_canvas.figure.axes[row].cla()
            self.waveform_canvas.figure.axes[row].plot(a.waveform_data
                                                       .transpose(1, 0, 2)
                                                       .reshape(a.waveform_data.shape[1], -1)[row], 'o', ms=2)

            self.waveform_canvas.figure.axes[row].set_xlabel('time, sample (x100ns)')
            self.waveform_canvas.figure.axes[row].set_ylabel('ADC channel')
            self.waveform_canvas.figure.axes[row].set_title(f'CH-{row} WaveForm')
            self.waveform_canvas.figure.axes[row].set_ylim(0, a.max_value[row] * 1.2)

        self.waveform_canvas.draw()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = WaveFormWindow()
    w.update_plot(filename='runs/385/1-385.txt')
    w.show()
    app.exec()
