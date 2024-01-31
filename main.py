import sys
from PySide6 import QtWidgets
import matplotlib
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
        axs[0][0].set_title('wave1')
        super().__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.figure.axes[1].set_title('wave2')
        filename_list = ['runs/385/1-385.txt','runs/385/2-385.txt','runs/385/3-385.txt','runs/385/4-385.txt','runs/385/5-385.txt']
        a = NWaveForm(full_filename=filename_list[0])

        for row in range(64):
            sc.figure.axes[row].plot(a.waveform_data
                                     .transpose(1, 0, 2)
                                     .reshape(a.waveform_data.shape[1], -1)[row], 'o', ms=2)
            # sc.figure.axes[row].set_ylim(0)
            sc.figure.axes[row].set_xlabel('time, sample (x100ns)')
            sc.figure.axes[row].set_ylabel('ADC channel')
            sc.figure.axes[row].set_title(f'CH-{row} WaveForm')
            sc.figure.axes[row].set_ylim(0, a.max_value[row] * 1.2)
        # sc.axes[1].plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        # Create toolbar, passing canvas as first parameter, parent(self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)
        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()
