import sys
from PySide6.QtWidgets import QPushButton, QMainWindow, QApplication, QLabel, QLineEdit, QWidget, QVBoxLayout

from waveform import NWaveForm
from waveform_window import WaveFormWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.waveform_window = WaveFormWindow()

        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.filename_label = QLabel("Filename:")
        self.filename_line_edit = QLineEdit()
        self.filename_line_edit.setPlaceholderText('runs/385/1-385.txt')
        self.filename_line_edit.setText('runs/385/1-385.txt')
        self.waveform_update_button = QPushButton("update")
        print(self.filename_line_edit.text())
        self.waveform_update_button.clicked.connect(self.update_waveform_window)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.filename_label)
        self.verticalLayout.addWidget(self.filename_line_edit)
        self.verticalLayout.addWidget(self.button)
        self.verticalLayout.addWidget(self.waveform_update_button)

        self.widget = QWidget()
        self.widget.setLayout(self.verticalLayout)
        self.setCentralWidget(self.widget)

        self.show()

    def update_waveform_window(self):
        self.waveform_window.update_plot(filename=self.filename_line_edit.text())
    def show_new_window(self, checked):
        self.waveform_window.show()


app = QApplication(sys.argv)
w = MainWindow()
app.exec()
