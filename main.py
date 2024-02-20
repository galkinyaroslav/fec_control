import json
import os.path
import re
import sys
import traceback

import numpy as np
from PySide6 import QtGui
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QIntValidator, QColor
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox

from fec import FEC, TestsName
from waveform import NWaveForm
from waveform_window import WaveFormWindow, RMSWindow
from MainWindow import Ui_MainWindow
from workers import Worker


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        host = '192.168.1.235'
        port = 30
        self.fe_card = FEC(host=host, port=port)
        self.threadpool = QThreadPool()

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
        self.__scan_pll_runs = self.scan_pll_runs_spinbox.value()
        self.__set_sh0_value = self.set_sh0_spinbox.value()
        self.__set_sh1_value = self.set_sh1_spinbox.value()

        self.link_spinBox.valueChanged.connect(self.link_value_changed)
        self.scan_pll_runs_spinbox.valueChanged.connect(self.scan_pll_runs_spinbox_changed)
        self.set_sh0_spinbox.valueChanged.connect(self.set_sh0_spinbox_changed)
        self.set_sh1_spinbox.valueChanged.connect(self.set_sh1_spinbox_changed)

        self.trstat_btn.clicked.connect(lambda: self.execute(fec_func=self.trstat_fc))
        self.ini_btn.clicked.connect(lambda: self.execute(fec_func=self.ini_fc))
        self.tts_tth_btn.clicked.connect(lambda: self.execute(fec_func=self.tts_tth_fc))
        self.scan_pll_btn.clicked.connect(lambda: self.execute(fec_func=self.scan_pll_fc))
        self.set_pll_btn.clicked.connect(lambda: self.execute(fec_func=self.set_pll_fc))
        self.adcd_btn.clicked.connect(lambda: self.execute(fec_func=self.adcd_fc))
        self.ttok_btn.clicked.connect(lambda: self.execute(fec_func=self.ttok_fc))
        self.raw_btn.clicked.connect(lambda: self.execute(fec_func=self.raw_fc))
        self.crosstalk_even_btn.clicked.connect(lambda: self.execute(fec_func=self.crosstalk_even_fc))
        self.crosstalk_odd_btn.clicked.connect(lambda: self.execute(fec_func=self.crosstalk_odd_fc))
        self.gain_btn.clicked.connect(lambda: self.execute(fec_func=self.gain_fc))
        self.pedestal_btn.clicked.connect(lambda: self.execute(fec_func=self.pedestal_fc))

        # CDET
        self.__enc_cdet = self.enc_cdet_comboBox.itemText(self.enc_cdet_comboBox.currentIndex())
        self.enc_cdet_comboBox.activated.connect(self.enc_cdet_activate)

        self.show()

    def execute(self, *args, **kwargs):
        # print(kwargs)
        worker = Worker(*args, **kwargs)
        worker.signals.finished.connect(self.on_telnet_finished)
        # Execute
        self.threadpool.start(worker)

    def on_telnet_finished(self, fec_func, result, *args, **kwargs):
        print(f'{fec_func.__name__} is finished')

    def get_path(self, test_name: TestsName = TestsName.RAW) -> str:
        return f'./runs/{self.__card_number}/{self.__enc_cdet}/{test_name.value}/'

    def get_file_number(self, test_name: TestsName = TestsName.RAW) -> int:
        path = self.get_path(test_name)
        if not os.path.exists(path):
            os.makedirs(path)
        return len(os.listdir(path)) + 1

    def raw_fc(self, data_filter: bool = True):
        adcd = self.fe_card.adcd(n=3, link=31)
        ff = []
        # ff1 = self.fe_card.getff(link=31)
        # ff2 = self.fe_card.getff(link=31)
        # ff.append(ff1)
        # ff.append(ff2)
        nrun = 1
        runs_number = 10
        while runs_number:
            received_data = self.fe_card.getff(link=self.__link)
            print(f'{received_data=}')
            print(f'Run #{nrun}, TTH>>{received_data[-3].decode()}\n')
            wform = NWaveForm(raw_data=received_data[1:-34])
            if not wform.check_data() and data_filter:
                runs_number += 1
            else:
                ff.append((b' '.join(b'0x' + word for word in received_data[1:-34])).decode())
            # events_file.write((b' '.join(b'0x' + word for word in received_data[1:-34]) + b'\n').decode())
            runs_number -= 1
            nrun += 1
        # oscmd(
        #     f'cp events.lst ./runs/{card_number}/{test_name.value}/{file_name}')  # TODO придумать как передавать имя теста 2

        # self.__plot_run_number = self.get_file_number(TestsName.RAW)
        # self.plot_run_number_lineEdit.setText(str(self.__plot_run_number))
        vatfilename = f'{self.get_file_number(TestsName.RAW)}-{self.__card_number}.vat'
        filename = f'{self.get_file_number(TestsName.RAW)}-{self.__card_number}.txt'

        path = self.get_path(test_name=TestsName.RAW)
        fullpath = path + filename
        vatfullpath = path + vatfilename
        header = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0', 'Tsam',
                  'Va2_1_25', 'mA3_S1', 'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']
        # with open(vatfullpath, 'w') as f:
        #     f.write(f'{' '.join(header)}\n',)
        # time.sleep(10)
        np.savetxt(vatfullpath, adcd, delimiter=' ', fmt='%.2f', header=f'{' '.join(header)}')
        if not os.path.exists(path):
            os.makedirs(path)
        with open(fullpath, 'w') as f:
            for line in ff:
                f.write(f'{line}\n')

    def ttok_fc(self):
        self.fe_card.ttok(self.ttok_lineEdit.text())

    def adcd_fc(self):
        self.fe_card.adcd(link=self.__link, n=self.adcd_number_spinBox.value())

    def set_pll_fc(self):
        response = self.fe_card.set_card_pll(link=self.__link,
                                             sh0=self.set_sh0_spinbox.value(),
                                             sh1=self.set_sh1_spinbox.value())
        self.tts_tth_led.setColor(QColor('green')) if response else self.tts_tth_led.setColor(QColor('red'))

    def scan_pll_fc(self):
        # fe_card.scan_card_pll(link=self.__link)
        card_number = self.fe_card.get_card_number(link=self.__link)
        file_number = self.get_file_number(test_name=TestsName.PLL)
        with open(f'{self.get_path(TestsName.PLL)}/{file_number}-{card_number}.pll', 'a') as pf:
            for i in range(self.__scan_pll_runs):
                pll_dict = self.fe_card.scan_card_pll(link=self.__link, runs=self.__scan_pll_runs)
                pf.write(str(pll_dict) + '\n')
                print(pll_dict)
                self.sh0_value_label.setText(pll_dict['sh0'])
                self.sh1_value_label.setText(pll_dict['sh1'])
        # return pll_dict

    def tts_tth_fc(self):
        return self.tts_tth_led.setColor(QColor('green')) \
            if self.fe_card.get_tts_tth(link=self.__link) \
            else self.tts_tth_led.setColor(QColor('red'))

    def ini_fc(self):
        self.fe_card.ini(link=self.__link)

    def trstat_fc(self):
        self.fe_card.ttok(f'wmsk 0xffffffff')
        self.fe_card.get_trstat(link=self.__link)
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
            if self.__card_number == 0:
                self.trstat_led.setColor(QColor('red'))
            else:
                self.trstat_led.setColor(QColor('green'))
            self.plot_card_number_lineEdit.setText(str(self.__card_number))
            self.__plot_card_number = self.__card_number

    def scan_pll_runs_spinbox_changed(self):
        self.__scan_pll_runs = self.scan_pll_runs_spinbox.value()

    def set_sh0_spinbox_changed(self):
        self.__set_sh0_value = self.set_sh0_spinbox.value()

    def set_sh1_spinbox_changed(self):
        self.__set_sh1_value = self.set_sh1_spinbox.value()

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

    def enc_cdet_activate(self, idx):
        self.__enc_cdet = self.enc_cdet_comboBox.itemText(idx)
        self.plot_cdet_comboBox.setCurrentIndex(idx)
        self.__plot_cdet = self.enc_cdet_comboBox.itemText(idx)
        # print(f'{self.__plot_cdet=}')
        # print(self.__enc_cdet)

    def plot_test_name_handler(self):
        match self.__plot_test_name:
            case 'rms_pedestal' | 'raw':
                return f'{self.__plot_run_number}-{self.__plot_card_number}.txt'
            case 'crosstalk':
                return f'{self.__plot_run_number}-{self.__plot_card_number}-{self.__plot_parity}-2pF.txt'
            case 'gain':
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

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.fe_card.tln.write('!\r\n'.encode('utf-8'))
            self.fe_card.tln.close()
            event.accept()
        else:
            event.ignore()


try:
    # np.set_printoptions(linewidth=1000, threshold=np.inf)

    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
except Exception as e:
    print(e)
    print(traceback.format_exc())
#
finally:

    # fe_card.tln.write('!\r\n'.encode('utf-8'))
    # fe_card.tln.close()
    print(f'RCU has been closed')
