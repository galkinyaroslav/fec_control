import fnmatch
import json
import os.path
import sys
import traceback
import time

import numpy as np
from PySide6.QtCore import QThreadPool, Slot
from PySide6.QtGui import QIntValidator, QColor, QDoubleValidator
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox

from fec import FEC, TestsName
from gen import AFG3152C
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

        self.gen = AFG3152C()
        self.gen.rst()
        time.sleep(1)
        self.gen.set_initial_parameters()

        self.threadpool = QThreadPool()

        # PLOTTING
        self.waveform_window = WaveFormWindow()
        self.rms_window = RMSWindow()

        # self.__plot_card_number = self.plot_card_number_lineEdit.placeholderText()
        # self.__plot_cdet = self.plot_cdet_comboBox.itemText(self.plot_cdet_comboBox.currentIndex())
        # self.__plot_test_name = self.plot_test_name_comboBox.itemText(self.plot_test_name_comboBox.currentIndex())
        # self.__plot_parity = self.plot_parity_comboBox.itemText(self.plot_parity_comboBox.currentIndex())
        # self.__plot_run_number = self.plot_run_number_lineEdit.placeholderText()
        # self.__plot_event_number = self.plot_event_number_lineEdit.placeholderText()
        # self.__plot_amplitude = self.plot_amplitude_lineEdit.placeholderText()

        # <<<--- INT VALIDATOR --->>>
        only_int = QIntValidator()
        # only_int.setRange(0, 4)
        self.plot_card_number_lineEdit.setValidator(only_int)
        self.plot_run_number_lineEdit.setValidator(only_int)
        self.plot_event_number_lineEdit.setValidator(only_int)

        float_only = QDoubleValidator()
        float_only.setRange(0.02, 0.5, 2)
        float_only.setNotation(QDoubleValidator.StandardNotation)
        self.plot_amplitude_lineEdit.setValidator(float_only)

        self.show_waveform_btn.clicked.connect(self.show_waveform_plot_window)
        self.show_rms_btn.clicked.connect(self.show_rms_plot_window)
        self.update_plots_btn.clicked.connect(self.update_plots_windows)

        # self.plot_cdet_comboBox.activated.connect(self.plot_cdet_activate)
        # self.plot_test_name_comboBox.activated.connect(self.plot_test_name_activate)
        # self.plot_parity_comboBox.activated.connect(self.plot_parity_activate)

        # self.plot_card_number_lineEdit.editingFinished.connect(self.plot_card_number_edit)
        # self.plot_run_number_lineEdit.editingFinished.connect(self.plot_run_number_edit)
        # self.plot_event_number_lineEdit.editingFinished.connect(self.plot_event_number_edit)
        # self.plot_amplitude_lineEdit.editingFinished.connect(self.plot_amplitude_edit)

        # BASIC COMMANDS
        self.__link = 31
        self.__card_number = None
        self.__pll = None
        self.__cid = None
        self.__rid = None
        self.__mask = None
        self.__scan_pll_runs = self.scan_pll_runs_spinbox.value()
        # self.__set_sh0_value = self.set_sh0_spinbox.value()
        # self.__set_sh1_value = self.set_sh1_spinbox.value()

        self.link_spinBox.valueChanged.connect(self.link_value_changed)
        self.scan_pll_runs_spinbox.valueChanged.connect(self.scan_pll_runs_spinbox_changed)
        # self.set_sh0_spinbox.valueChanged.connect(self.set_sh0_spinbox_changed)
        # self.set_sh1_spinbox.valueChanged.connect(self.set_sh1_spinbox_changed)

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
                                                              sh0=self.set_sh0_spinbox.value(),
                                                              sh1=self.set_sh1_spinbox.value()
                                                              ))
        self.adcd_btn.clicked.connect(lambda: self.execute(run_func=self.adcd_fc,
                                                           fecard=self.fe_card,
                                                           link=self.__link,
                                                           n=self.adcd_number_spinBox.value()
                                                           ))
        self.ttok_btn.clicked.connect(lambda: self.execute(run_func=self.ttok_fc,
                                                           fecard=self.fe_card,
                                                           ))

        # CROSSTALK EVEN
        self.crosstalk_btn.clicked.connect(lambda: self.execute(run_func=self.crosstalk_fc,
                                                                fecard=self.fe_card,
                                                                gen=self.gen,
                                                                data_filter=True,
                                                                link=self.__link))

        # GAIN
        self.gain_btn.clicked.connect(lambda: self.execute(run_func=self.gain_fc,
                                                           fecard=self.fe_card,
                                                           gen=self.gen,
                                                           data_filter=True,
                                                           link=self.__link
                                                           ))
        # RMS_PEDESTAL
        self.pedestal_btn.clicked.connect(lambda: self.execute(run_func=self.rms_pedestal_fc,
                                                               fecard=self.fe_card,
                                                               data_filter=True,
                                                               link=self.__link))

        # CDET
        self.__enc_cdet = self.enc_cdet_comboBox.itemText(self.enc_cdet_comboBox.currentIndex())
        self.enc_cdet_comboBox.activated.connect(self.enc_cdet_activate)

        # RAW
        self.__raw_runs = self.raw_runs_spinBox.value()
        self.raw_runs_spinBox.valueChanged.connect(self.raw_runs_spinbox_changed)
        self.raw_btn.clicked.connect(lambda: self.execute(run_func=self.raw_fc,
                                                          fecard=self.fe_card,
                                                          runs_number=self.__raw_runs,
                                                          data_filter=True,
                                                          link=self.__link
                                                          ))

        self.show()

    def execute(self, *args, **kwargs):
        # print(kwargs)
        worker = Worker(*args, **kwargs)
        worker.signals.finished.connect(self.onTelnetFinished)
        # Execute
        self.threadpool.start(worker)

    @Slot(object, object, object)
    def onTelnetFinished(self, fec_func, result, *args, **kwargs):
        print(f'{fec_func.__name__} is finished\n')
        match fec_func.__name__:
            case 'rms_pedestal_fc':
                file_number = self.get_file_number(TestsName.RMS_PEDESTAL)
                vatfilename = f'{file_number}-{self.__card_number}.vat'
                filename = f'{file_number}-{self.__card_number}.txt'
                path = self.get_path(test_name=TestsName.RMS_PEDESTAL)
                fullpath = path + filename
                vatfullpath = path + vatfilename
                header = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0',
                          'Tsam', 'Va2_1_25', 'mA3_S1', 'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']
                np.savetxt(vatfullpath, result['adcd'], delimiter=' ', fmt='%.2f', header=f'{' '.join(header)}')
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(fullpath, 'w') as f:
                    for line in result['ff']:
                        f.write((b' '.join(b'0x' + word for word in line) + b'\n').decode())

                self.pedestal_lastrun_label.setText(f'{fullpath}')
                self.plot_run_number_lineEdit.setText(str(file_number))
                self.plot_test_name_comboBox.setCurrentIndex(self.plot_test_name_comboBox.findText('rms_pedestal'))
            case 'crosstalk_fc':
                file_number = self.get_file_number(TestsName.CROSSTALK)
                vatfilename = f'{file_number}-{self.__card_number}.vat'
                path = self.get_path(test_name=TestsName.CROSSTALK)
                vatfullpath = path + vatfilename
                header = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0',
                          'Tsam', 'Va2_1_25', 'mA3_S1', 'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']
                np.savetxt(vatfullpath, result['adcd'], delimiter=' ', fmt='%.2f', header=f'{' '.join(header)}')
                for gen_channel in range(1, 3, 1):
                    parity = 'even' if gen_channel == 1 else 'odd'
                    filename = f'{file_number}-{self.__card_number}-{parity}-2pF.txt'
                    fullpath = path + filename

                    if not os.path.exists(path):
                        os.makedirs(path)
                    with open(fullpath, 'w') as f:
                        for line in result['ff'][gen_channel - 1]:
                            f.write((b' '.join(b'0x' + word for word in line) + b'\n').decode())

                    self.crosstalk_lastrun_label.setText(f'{fullpath}')
                    self.plot_run_number_lineEdit.setText(str(file_number))
                    self.plot_test_name_comboBox.setCurrentIndex(self.plot_test_name_comboBox.findText('crosstalk'))

            case 'gain_fc':
                ampl_range = np.linspace(0.02, 0.6, 30)
                file_number = self.get_file_number(TestsName.GAIN)
                vatfilename = f'{file_number}-{self.__card_number}-2pF.vat'
                path = self.get_path(test_name=TestsName.GAIN)
                vatfullpath = path + vatfilename
                header = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0',
                          'Tsam', 'Va2_1_25', 'mA3_S1', 'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']
                np.savetxt(vatfullpath, result['adcd'], delimiter=' ', fmt='%.2f', header=f'{' '.join(header)}')
                for ampl in range(len(ampl_range)):

                    filename = f'{file_number}-{self.__card_number}-2pF-{round(ampl_range[ampl], 2)}V.txt'
                    fullpath = path + filename

                    if not os.path.exists(path):
                        os.makedirs(path)
                    with open(fullpath, 'w') as f:
                        for line in result['ff'][ampl]:
                            f.write((b' '.join(b'0x' + word for word in line) + b'\n').decode())
                    self.gain_lastrun_label.setText(f'{fullpath}')
                    self.plot_run_number_lineEdit.setText(str(file_number))
                    self.plot_test_name_comboBox.setCurrentIndex(self.plot_test_name_comboBox.findText('gain'))
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
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(fullpath, 'w') as f:
                    for line in result['ff']:
                        f.write((b' '.join(b'0x' + word for word in line) + b'\n').decode())

                self.raw_lastrun_label.setText(f'{fullpath}')
                self.plot_run_number_lineEdit.setText(str(file_number))
                self.plot_test_name_comboBox.setCurrentIndex(self.plot_test_name_comboBox.findText('raw'))

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
                    pll = dict({'sh0': str(data['sh0']), 'sh1': str(data['sh1'])})
                    self.__pll = pll['sh0'] + ', ' + pll['sh1']
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
                    # self.__plot_card_number = self.__card_number
                path = self.get_path(test_name=TestsName.PLL)
                fullname = path + f'{self.__card_number}_in_memory_pll.json'
                if not os.path.exists(fullname):
                    if not os.path.exists(path):
                        os.makedirs(path)
                    with open(fullname, 'w') as f:
                        json.dump(pll, f)
            case _:
                raise ValueError(f'{fec_func.__name__} is not appropriate')

    def get_path(self, test_name: TestsName = TestsName.RAW) -> str:
        return f'./runs/{self.__card_number}/{self.__enc_cdet}/{test_name.value}/'

    def get_file_number(self, test_name: TestsName = TestsName.RAW) -> int:
        path = self.get_path(test_name)
        if not os.path.exists(path):
            os.makedirs(path)
        numfile = len(fnmatch.filter(os.listdir(path), '*.txt'))
        match test_name.value:
            case TestsName.PLL.value:
                return numfile + 1
            case TestsName.RAW.value | TestsName.RMS_PEDESTAL.value:
                return numfile + 1
            case TestsName.GAIN.value:
                return int(-(numfile // -25)) + 1 if numfile else 1  # 25 - len(input amplitudes)
            case TestsName.CROSSTALK.value:
                return int(-(numfile // -2)) + 1 if numfile else 1  # 2 for odd and even
            case _:
                raise ValueError(f'{test_name.value} is not in TestsName')

    def rms_pedestal_fc(self, fecard, link: int = 31, data_filter: bool = True):
        runs_number: int = 100
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

    def crosstalk_fc(self, fecard, gen, link: int = 31, data_filter: bool = True):
        """gen 1,2 channels"""
        adcd = fecard.adcd(n=3, link=link)
        ff = []
        gen.set_output_state('OFF', channel=1)
        gen.set_output_state('OFF', channel=2)

        for gen_channel in range(1, 3, 1):
            runs_number = 10

            gen.set_volt_low(low=0, channel=gen_channel)
            gen.set_volt_high(high=0.5, channel=gen_channel)
            gen.set_output_state('ON', channel=gen_channel)
            time.sleep(1)
            nrun = 1
            ff.append([])
            while runs_number:
                received_data = fecard.getff(link=link)
                print(f'Run #{nrun}, TTH>>{received_data[-3].decode()}\n')
                wform = NWaveForm(raw_data=received_data[1:-34])
                if not wform.check_data() and data_filter:
                    runs_number += 1
                else:
                    ff[gen_channel - 1].append(received_data[1:-34])
                runs_number -= 1
                nrun += 1
            gen.set_output_state('OFF', channel=gen_channel)

        return {'adcd': adcd, 'ff': ff}

    def gain_fc(self, fecard, gen, link: int = 31, data_filter: bool = True):
        adcd = fecard.adcd(n=3, link=link)
        ff = []
        ampl_range = np.linspace(0.02, 0.6, 30)

        for ampl in range(len(ampl_range)):
            runs_number = 10
            print(f'{ampl=}')
            gen.set_volt_low(low=0)
            gen.set_volt_high(high=round(ampl_range[ampl], 2))
            gen.set_volt_low(low=0, channel=2)
            gen.set_volt_high(high=round(ampl_range[ampl], 2), channel=2)
            gen.set_output_state('ON', channel=2)
            gen.set_output_state('ON', channel=1)
            time.sleep(1)
            ff.append([])
            nrun = 1
            while runs_number:
                received_data = fecard.getff(link=link)
                print(f'Run #{nrun}, TTH>>{received_data[-3].decode()}\n')
                wform = NWaveForm(raw_data=received_data[1:-34])
                if not wform.check_data() and data_filter:
                    runs_number += 1
                else:
                    ff[ampl].append(received_data[1:-34])
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

    # def set_sh0_spinbox_changed(self):
    #     self.__set_sh0_value = self.set_sh0_spinbox.value()
    #
    # def set_sh1_spinbox_changed(self):
    #     self.__set_sh1_value = self.set_sh1_spinbox.value()

    def link_value_changed(self):
        self.__link = self.link_spinBox.value()

    # def plot_amplitude_edit(self):
    #     self.__plot_amplitude = self.plot_amplitude_lineEdit.text()
    #
    # def plot_event_number_edit(self):
    #     self.__plot_event_number = self.plot_event_number_lineEdit.text()
    #
    # def plot_run_number_edit(self):
    #     self.__plot_run_number = self.plot_run_number_lineEdit.text()

    # def plot_card_number_edit(self):
    #     self.__plot_card_number = self.plot_card_number_lineEdit.text()

    # def plot_parity_activate(self, idx):
        # self.__plot_parity = self.plot_parity_comboBox.itemText(idx)

    # def plot_test_name_activate(self, idx):
        # self.__plot_test_name = self.plot_test_name_comboBox.itemText(idx)

    # def plot_cdet_activate(self, idx):
    #     self.__plot_cdet = self.plot_cdet_comboBox.itemText(idx)

    def enc_cdet_activate(self, idx):
        # self.__enc_cdet = self.enc_cdet_comboBox.itemText(idx)
        self.plot_cdet_comboBox.setCurrentIndex(idx)
        # self.__plot_cdet = self.enc_cdet_comboBox.itemText(idx)

    def plot_test_name_handler(self):
        match self.plot_test_name_comboBox.currentText():
            case 'rms_pedestal' | 'raw':
                return f'{self.plot_run_number_lineEdit.text()}-{self.plot_card_number_lineEdit.text()}.txt'
            case 'crosstalk':
                return f'{self.plot_run_number_lineEdit.text()}-{self.plot_card_number_lineEdit.text()}-{self.plot_parity_comboBox.currentText()}-2pF.txt'
            case 'gain':
                return f'{self.plot_run_number_lineEdit.text()}-{self.plot_card_number_lineEdit.text()}-2pF-{self.plot_amplitude_lineEdit.text()}V.txt'
            case _:
                raise ValueError(f'No such test: {self.plot_test_name_comboBox.currentText()}')
                # return None

    def update_plots_windows(self):
        filename = self.plot_test_name_handler()
        fullpath = (f'runs/'
                    f'{self.plot_card_number_lineEdit.text()}/'
                    f'{self.plot_cdet_comboBox.currentText()}/'
                    f'{self.plot_test_name_comboBox.currentText()}/'
                    f'{filename}')
        if os.path.exists(fullpath):
            try:
                self.waveform_window.update_plot(filename=fullpath, event=int(self.plot_event_number_lineEdit.text()))
                self.rms_window.update_plot(filename=fullpath, event=int(self.plot_event_number_lineEdit.text()))
                self.plot_file_exist_label.setText(f'{fullpath} has been plotted')
                self.plot_file_exist_label.setStyleSheet('color: green;')
            except ValueError as e:
                self.plot_file_exist_label.setText(f'ValueError {e}')
                self.plot_file_exist_label.setStyleSheet('color: red;')
                print(traceback.format_exc())
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
