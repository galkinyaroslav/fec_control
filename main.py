import sys
from PySide6.QtWidgets import QPushButton, QMainWindow, QApplication, QLabel, QLineEdit, QWidget, QVBoxLayout

from waveform import NWaveForm
from waveform_window import WaveFormWindow, RMSWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.waveform_window = WaveFormWindow()
        self.rms_window = RMSWindow()
        self.show_waveform_button = QPushButton("Show WaveForm")
        self.show_rms_button = QPushButton("Show RMS")
        self.filename_label = QLabel("Filename:")
        self.filename_line_edit = QLineEdit()
        self.filename_line_edit.setPlaceholderText('runs/385/4-385.txt')
        self.filename_line_edit.setText('runs/385/4-385.txt')
        self.plots_update_button = QPushButton("Update")
        print(self.filename_line_edit.text())

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.filename_label)
        self.verticalLayout.addWidget(self.filename_line_edit)
        self.verticalLayout.addWidget(self.show_waveform_button)
        self.verticalLayout.addWidget(self.show_rms_button)
        self.verticalLayout.addWidget(self.plots_update_button)

        self.show_waveform_button.clicked.connect(self.show_waveform_plot_window)
        self.show_rms_button.clicked.connect(self.show_rms_plot_window)

        self.plots_update_button.clicked.connect(self.update_plots_windows)

        self.widget = QWidget()
        self.widget.setLayout(self.verticalLayout)
        self.setCentralWidget(self.widget)

        self.show()

    def update_plots_windows(self):
        self.waveform_window.update_plot(filename=self.filename_line_edit.text())
        self.rms_window.update_plot(filename=self.filename_line_edit.text())

    def show_waveform_plot_window(self, checked):
        if self.waveform_window.isVisible():
            self.waveform_window.hide()
        else:
            self.waveform_window.show()

    def show_rms_plot_window(self, checked):
        if self.rms_window.isVisible():
            self.rms_window.hide()
        else:
            self.rms_window.show()


app = QApplication(sys.argv)
w = MainWindow()
app.exec()
