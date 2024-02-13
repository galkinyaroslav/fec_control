import os.path
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator, QFont
from PySide6.QtWidgets import QMainWindow, QApplication

from waveform import NWaveForm
from waveform_window import WaveFormWindow, RMSWindow
from MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.waveform_window = WaveFormWindow()
        self.rms_window = RMSWindow()

        self.__plot_card_number = self.plot_card_number_lineEdit.placeholderText()
        self.__plot_cdet = self.plot_cdet_comboBox.itemText(self.plot_cdet_comboBox.currentIndex())
        self.__plot_test_name = self.plot_test_name_comboBox.itemText(self.plot_test_name_comboBox.currentIndex())
        print(f'{self.__plot_test_name}')
        self.__plot_parity = self.plot_parity_comboBox.itemText(self.plot_parity_comboBox.currentIndex())
        self.__plot_run_number = self.plot_run_number_lineEdit.placeholderText()
        self.__plot_event_number = self.plot_event_number_lineEdit.placeholderText()
        self.__plot_amplitude = self.plot_amplitude_lineEdit.placeholderText()

        # <<<--- INT VALIDATOR --->>>
        only_int = QIntValidator()
        # only_int.setRange(0, 4)
        self.plot_card_number_lineEdit.setValidator(only_int)
        self.plot_run_number_lineEdit.setValidator(only_int)
        self.plot_event_number_lineEdit.setValidator(only_int)
        self.plot_amplitude_lineEdit.setValidator(only_int)

        self.show_waveform_btn.clicked.connect(self.show_waveform_plot_window)
        self.show_rms_btn.clicked.connect(self.show_rms_plot_window)
        self.update_plots_btn.clicked.connect(self.update_plots_windows)

        self.plot_cdet_comboBox.activated.connect(self.plot_cdet_activate)
        self.plot_test_name_comboBox.activated.connect(self.plot_test_name_activate)
        self.plot_parity_comboBox.activated.connect(self.plot_parity_activate)

        self.plot_card_number_lineEdit.editingFinished.connect(self.plot_card_number_edit)
        self.plot_run_number_lineEdit.editingFinished.connect(self.plot_run_number_edit)
        self.plot_event_number_lineEdit.editingFinished.connect(self.plot_event_number_edit)
        self.plot_amplitude_lineEdit.editingFinished.connect(self.plot_amplitude_edit)

        self.show()

    def plot_amplitude_edit(self):
        self.__plot_amplitude = self.plot_amplitude_lineEdit.text()
        print(self.__plot_amplitude)

    def plot_event_number_edit(self):
        self.__plot_event_number = self.plot_event_number_lineEdit.text()
        print(self.__plot_event_number)

    def plot_run_number_edit(self):
        self.__plot_run_number = self.plot_run_number_lineEdit.text()
        print(self.__plot_run_number)

    def plot_card_number_edit(self):
        self.__plot_card_number = self.plot_card_number_lineEdit.text()
        print(self.__plot_card_number)

    def plot_parity_activate(self, idx):
        self.__plot_parity = self.plot_parity_comboBox.itemText(idx)
        print(self.__plot_parity)

    def plot_test_name_activate(self, idx):
        self.__plot_test_name = self.plot_test_name_comboBox.itemText(idx)
        print(self.__plot_test_name)

    def plot_cdet_activate(self, idx):
        self.__plot_cdet = self.plot_cdet_comboBox.itemText(idx)
        print(self.__plot_cdet)

    def plot_test_name_handler(self):
        match self.__plot_test_name:
            case 'RMS_PEDESTAL' | 'RAW':
                return f'{self.__plot_run_number}-{self.__plot_card_number}.txt'
            case 'CROSSTALK':
                return f'{self.__plot_run_number}-{self.__plot_card_number}-{self.__plot_parity}-2pF.txt'
            case 'GAIN':
                return f'{self.__plot_run_number}-{self.__plot_card_number}-{self.__plot_amplitude}.txt'
            case _:
                raise ValueError(f'No such test: {self.__plot_test_name}')
                # return None

    def update_plots_windows(self):
        filename = self.plot_test_name_handler()
        print(f'{self.__plot_test_name=}')

        print(f'{filename=}')
        # filename = f'{self.__plot_run_number}-{self.__plot_card_number}.txt'
        fullpath = (f'runs/'
                    f'{self.__plot_card_number}/'
                    f'{self.__plot_cdet}/'
                    f'{self.__plot_test_name}/'
                    f'{filename}')
        if os.path.exists(fullpath):
            self.waveform_window.update_plot(filename=fullpath)
            self.rms_window.update_plot(filename=fullpath)
            self.plot_file_exist_label.setText(f'{fullpath} has been plotted')
            self.plot_file_exist_label.setStyleSheet('color: green;')
        else:
            self.plot_file_exist_label.setText(f'{fullpath} does not exist')
            self.plot_file_exist_label.setStyleSheet('color: red;')

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
