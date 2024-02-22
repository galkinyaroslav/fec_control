import fnmatch
import json
import os.path
import sys
import traceback

import numpy as np
from PySide6.QtCore import QThreadPool, Slot
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

        self.trstat_btn.clicked.connect(lambda: self.execute(run_func=self.trstat_fc,
                                                             fecard=self.fe_card,
                                                             link=self.__link))
        self.ini_btn.clicked.connect(lambda: self.execute(run_func=self.ini_fc,
                                                          fecard=self.fe_card,
                                                          link=self.__link))
        self.tts_tth_btn.clicked.connect(lambda: self.execute(run_func=self.tts_tth_fc,
                                                              fecard=self.fe_card,
                                                              link=self.__link

                                                              ))
        self.scan_pll_btn.clicked.connect(lambda: self.execute(run_func=self.scan_pll_fc,
                                                               fecard=self.fe_card,
                                                               link=self.__link,
                                                               runs=self.__scan_pll_runs
                                                               ))
        self.set_pll_btn.clicked.connect(lambda: self.execute(run_func=self.set_pll_fc,
                                                              fecard=self.fe_card,
                                                              link=self.__link,
                                                              sh0=self.__set_sh0_value,
                                                              sh1=self.__set_sh1_value
                                                              ))
        self.adcd_btn.clicked.connect(lambda: self.execute(run_func=self.adcd_fc,
                                                           fecard=self.fe_card,
                                                           link=self.__link,
                                                           n=self.adcd_number_spinBox.value()
                                                           ))
        self.ttok_btn.clicked.connect(lambda: self.execute(run_func=self.ttok_fc,
                                                           fecard=self.fe_card,
                                                           ))

        # self.crosstalk_even_btn.clicked.connect(lambda: self.execute(fec_func=self.crosstalk_even_fc))
        # self.crosstalk_odd_btn.clicked.connect(lambda: self.execute(fec_func=self.crosstalk_odd_fc))
        # self.gain_btn.clicked.connect(lambda: self.execute(fec_func=self.gain_fc))
        # self.pedestal_btn.clicked.connect(lambda: self.execute(fec_func=self.pedestal_fc))

        # CDET
        self.__enc_cdet = self.enc_cdet_comboBox.itemText(self.enc_cdet_comboBox.currentIndex())
        self.enc_cdet_comboBox.activated.connect(self.enc_cdet_activate)

        # RAW
        self.__raw_runs = self.raw_runs_spinBox.value()
        self.raw_runs_spinBox.valueChanged.connect(self.raw_runs_spinbox_changed)
        self.raw_btn.clicked.connect(lambda: self.execute(run_func=self.raw_fc,
                                                          fecard=self.fe_card,
                                                          runs_number=self.__raw_runs,
                                                          data_filter=False,
                                                          link=self.__link
                                                          ))

        self.show()

    def execute(self, *args, **kwargs):
        # print(kwargs)
        worker = Worker(*args, **kwargs)
        worker.signals.finished.connect(self.on_telnet_finished)
        # Execute
        self.threadpool.start(worker)


    @Slot(object, object, object)
    def on_telnet_finished(self, fec_func, result, *args, **kwargs):
        print(f'{fec_func.__name__} is finished\n')
        match fec_func.__name__:
            case 'raw_fc':
                file_number = self.get_file_number(TestsName.RAW)
                vatfilename = f'{file_number}-{self.__card_number}.vat'
                filename = f'{file_number}-{self.__card_number}.txt'
                path = self.get_path(test_name=TestsName.RAW)
                fullpath = path + filename
                vatfullpath = path + vatfilename
                header = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0',
                          'Tsam', 'Va2_1_25', 'mA3_S1', 'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']
                np.savetxt(vatfullpath, result['adcd'], delimiter=' ', fmt='%.2f', header=f'{' '.join(header)}')
                self.raw_lastrun_label.setText(f'{fullpath}')
                self.__plot_run_number = file_number
                self.plot_run_number_lineEdit.setText(str(self.__plot_run_number))

                if not os.path.exists(path):
                    os.makedirs(path)
                with open(fullpath, 'w') as f:
                    for line in result['ff']:
                        f.write((b' '.join(b'0x' + word for word in line) + b'\n').decode())
            case 'ttok_fc':
                pass
            case 'adcd_fc':
                pass
            case 'set_pll_fc':
                self.tts_tth_led.setColor(QColor('green')) \
                    if result else self.tts_tth_led.setColor(QColor('red'))

            case 'scan_pll_fc':
                card_number = self.fe_card.get_card_number(link=self.__link)
                file_number = self.get_file_number(test_name=TestsName.PLL)
                with open(f'{self.get_path(TestsName.PLL)}/{file_number}-{card_number}.pll', 'a') as pf:
                    for i in result:
                        pf.write(str(i) + '\n')
                        print(i)
                self.sh0_value_label.setText(result[0]['sh0'])
                self.sh1_value_label.setText(result[0]['sh1'])
                self.tts_tth_led.setColor(QColor('red'))

            case 'tts_tth_fc':
                self.tts_tth_led.setColor(QColor('green')) \
                        if result else self.tts_tth_led.setColor(QColor('red'))
            case 'ini_fc':
                pass

            case 'trstat_fc':
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
            case _:
                raise ValueError(f'{fec_func.__name__} is not appropriate')

    def get_path(self, test_name: TestsName = TestsName.RAW) -> str:
        return f'./runs/{self.__card_number}/{self.__enc_cdet}/{test_name.value}/'

    def get_file_number(self, test_name: TestsName = TestsName.RAW) -> int:
        path = self.get_path(test_name)
        if not os.path.exists(path):
            os.makedirs(path)
        match test_name.value:
            case TestsName.PLL.value:
                return len(fnmatch.filter(os.listdir(path), '*.pll')) + 1
            case TestsName.RAW.value | TestsName.GAIN.value | TestsName.RMS_PEDESTAL.value:
                return len(fnmatch.filter(os.listdir(path), '*.txt')) + 1
            case TestsName.CROSSTALK.value:
                return int(-(len(fnmatch.filter(os.listdir(path), '*.txt')) // -2)) + 1
            case _:
                raise ValueError(f'{test_name.value} is not in TestsName')

    def raw_fc(self, fecard, runs_number: int = 10, link: int = 31, data_filter: bool = True):
        adcd = fecard.adcd(n=3, link=link)
        ff = []
        nrun = 1
        while runs_number:
            received_data = fecard.getff(link=link)
            print(f'Run #{nrun}, TTH>>{received_data[-3].decode()}\n')
            wform = NWaveForm(raw_data=received_data[1:-34])
            if not wform.check_data() and data_filter:
                runs_number += 1
            else:
                ff.append(received_data[1:-34])
            runs_number -= 1
            nrun += 1
        return {'adcd': adcd, 'ff': ff}

    def ttok_fc(self, fecard, command):
        fecard.ttok(command=command)
        return None

    def adcd_fc(self, fecard, link: int = 31, n: int = 1):
        fecard.adcd(link=link, n=n)
        return None

    def set_pll_fc(self, fecard, link: int = 31, sh0: int = 0, sh1: int = 0):
        return fecard.set_card_pll(link=link, sh0=sh0, sh1=sh1)

    def scan_pll_fc(self, fecard, link: int = 31, runs: int = 1):
        pll_list_dict = []
        for i in range(runs):
            pll_list_dict.append(fecard.scan_card_pll(link=link))
        return pll_list_dict

    def tts_tth_fc(self, fecard, link: int = 31) -> bool:
        return fecard.get_tts_tth(link=link)

    def ini_fc(self, fecard, link: int = 31) -> None:
        fecard.ini(link=link)
        return None

    def trstat_fc(self, fecard, link: int = 31) -> dict:
        fecard.ttok(f'wmsk 0xffffffff')
        return fecard.get_trstat(link=link)

    def raw_runs_spinbox_changed(self):
        self.__raw_runs = self.raw_runs_spinBox.value()

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

    def plot_event_number_edit(self):
        self.__plot_event_number = self.plot_event_number_lineEdit.text()

    def plot_run_number_edit(self):
        self.__plot_run_number = self.plot_run_number_lineEdit.text()

    def plot_card_number_edit(self):
        self.__plot_card_number = self.plot_card_number_lineEdit.text()

    def plot_parity_activate(self, idx):
        self.__plot_parity = self.plot_parity_comboBox.itemText(idx)

    def plot_test_name_activate(self, idx):
        self.__plot_test_name = self.plot_test_name_comboBox.itemText(idx)

    def plot_cdet_activate(self, idx):
        self.__plot_cdet = self.plot_cdet_comboBox.itemText(idx)

    def enc_cdet_activate(self, idx):
        self.__enc_cdet = self.enc_cdet_comboBox.itemText(idx)
        self.plot_cdet_comboBox.setCurrentIndex(idx)
        self.__plot_cdet = self.enc_cdet_comboBox.itemText(idx)

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
        fullpath = (f'runs/'
                    f'{self.__plot_card_number}/'
                    f'{self.__plot_cdet}/'
                    f'{self.__plot_test_name}/'
                    f'{filename}')
        if os.path.exists(fullpath):
            try:
                self.waveform_window.update_plot(filename=fullpath, event=int(self.__plot_event_number))
                self.rms_window.update_plot(filename=fullpath, event=int(self.__plot_event_number))
                self.plot_file_exist_label.setText(f'{fullpath} has been plotted')
                self.plot_file_exist_label.setStyleSheet('color: green;')
            except ValueError as e:
                self.plot_file_exist_label.setText(f'ValueError {e}')
                self.plot_file_exist_label.setStyleSheet('color: red;')
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
            self.waveform_window.close()
            self.rms_window.close()
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
finally:
    print(f'RCU has been closed')
