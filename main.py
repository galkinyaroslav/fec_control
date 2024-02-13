import json
import os.path
import sys
import telnetlib
import traceback

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator, QFont
from PySide6.QtWidgets import QMainWindow, QApplication

from fec import FEC
from waveform import NWaveForm
from waveform_window import WaveFormWindow, RMSWindow
from MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # PLOTTING
        self.waveform_window = WaveFormWindow()
        self.rms_window = RMSWindow()

        self.__plot_card_number = self.plot_card_number_lineEdit.placeholderText()
        self.__plot_cdet = self.plot_cdet_comboBox.itemText(self.plot_cdet_comboBox.currentIndex())
        self.__plot_test_name = self.plot_test_name_comboBox.itemText(self.plot_test_name_comboBox.currentIndex())
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

        # BASIC COMMANDS
        self.__link = 31
        self.__card_number = None
        self.__pll = None
        self.__cid = None
        self.__rid = None
        self.__mask = None
        self.link_spinBox.valueChanged.connect(self.link_value_changed)

        self.trstat_btn.clicked.connect(self.trstat_fc)

        self.show()

    def trstat_fc(self, pressed):
        fe_card.ttok(f'wmsk 0xffffffff')
        fe_card.get_trstat(link=self.__link)
        with open('current_fec_trstats.json', 'r') as f:
            data = json.load(f)
            self.__card_number = data['card']
            self.__pll = str(data['sh0']) + ', ' + str(data['sh1'])
            self.__cid = data['cid']
            self.__rid = data['rid']
            self.__mask = data['mask']
            self.card_number_value_label.setText(str(self.__card_number))
            self.pll_value_label.setText(str(self.__pll))
            self.cid_value_label.setText(str(self.__cid))
            self.rid_value_label.setText(str(self.__rid))
            self.mask_value_label.setText(str(self.__mask))


    def link_value_changed(self):
        self.__link = self.link_spinBox.value()

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



host = '192.168.1.235'
port = 30
# tln = telnetlib.Telnet(timeout=10)
# tln.open(host=host, port=port)
# out = tln.read_until('return:\n\r'.encode('utf-8'), timeout=10)
# print(out.decode('utf-8'))
fe_card = FEC(host=host, port=port)

try:
    # np.set_printoptions(linewidth=1000, threshold=np.inf)


    # link = 31
    # fec.ttok(f'wmsk 0xffffffff')
    # fec.get_trstat(link=link)
    # fec.ini(link=link)
    # asd = fec.adcd(link=link, n=10)
    # fec.getffw(link=link, runs_number=1, single=True)

    # print(f'{asd=}')
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
except Exception as e:
    print(e)
    print(traceback.format_exc())

finally:
    fe_card.tln.write('!\r\n'.encode('utf-8'))
    fe_card.tln.close()



