import fnmatch
import json
# import os.path
import sys
import traceback
import time
from pathlib import Path

import numpy as np
from PySide6.QtCore import QThreadPool, Slot, Signal
from PySide6.QtGui import QIntValidator, QColor, QDoubleValidator
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox

from app.config import RUNS_DIR, DATA_DIR
from app.logic.fec import TestsName, FEC, get_card_number, get_card_fw
from app.logic.gen import AFG3152C
from app.logic.data_structure.factory import NWaveForm
from app.widgets.connection import ConnectionForm
from app.windows.waveform_window import WaveFormWindow, RMSWindow
from app.ui.MainWindow_UI import Ui_MainWindow
from app.logic.workers import Worker

FW_DATA_LENGTH = {'0x24040800': 778,
                  '0x23040600': 768,
                  '0x23040400': 768}


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.connection_widget = None

        self.fe_card: FEC | None = None
        self.gen: AFG3152C | None = None

        self.threadpool = QThreadPool()
        self.worker = None

        # PLOTTING
        self.waveform_window = WaveFormWindow()
        self.rms_window = RMSWindow()
        for button in self.buttonGroup.buttons():
            button.setEnabled(False)
        self.actionConnections.triggered.connect(self.open_connection_widget)

        for button in self.buttonGroup.buttons():
            button.clicked.connect(self.on_button_clicked)

        self.__plot_cdet = self.plot_cdet_comboBox.itemText(self.plot_cdet_comboBox.currentIndex())

        # <<<--- INT VALIDATOR --->>>
        only_int = QIntValidator()
        self.plot_card_number_lineEdit.setValidator(only_int)
        self.plot_run_number_lineEdit.setValidator(only_int)
        self.plot_event_number_lineEdit.setValidator(only_int)

        self.show_waveform_btn.clicked.connect(self.show_waveform_plot_window)
        self.show_rms_btn.clicked.connect(self.show_rms_plot_window)
        self.update_plots_btn.clicked.connect(self.update_plots_windows)

        # BASIC COMMANDS
        self.__link = 31
        self.__card_number = None
        self.__pll = None
        self.__cid = None
        self.__rid = None
        self.__mask = None
        self.__scan_pll_runs = self.scan_pll_runs_spinbox.value()

        self.link_spinBox.valueChanged.connect(self.link_value_changed)
        self.scan_pll_runs_spinbox.valueChanged.connect(self.scan_pll_runs_spinbox_changed)
        # # RAW
        self.__raw_runs = self.raw_runs_spinBox.value()
        self.raw_runs_spinBox.valueChanged.connect(self.raw_runs_spinbox_changed)

        # CDET
        self.__enc_cdet = self.enc_cdet_comboBox.itemText(self.enc_cdet_comboBox.currentIndex())
        self.enc_cdet_comboBox.activated.connect(self.enc_cdet_activate)

        self.stop_thread_btn.clicked.connect(self.break_thread)
        self.stop_thread_flag = False

        self.button_functions = {
            'pedestal_btn': self.rms_pedestal_fc,
            'gain_cross_odd_btn': self.gain_cross_fc,
            'gain_cross_even_btn': self.gain_cross_fc,
            'raw_btn': self.raw_fc,
            'ttok_btn': self.ttok_fc,
            'adcd_btn': self.adcd_fc,
            'set_pll_btn': self.set_pll_fc,
            'scan_pll_btn': self.scan_pll_fc,
            'tts_tth_btn': self.tts_tth_fc,
            'ini_btn': self.ini_fc,
            'trstat_btn': self.trstat_fc,

        }
        self.current_args = {
            'pedestal_btn': None,
            'gain_cross_odd_btn': None,
            'gain_cross_even_btn': None,
            'raw_btn': None,
            'ttok_btn': None,
            'adcd_btn': None,
            'set_pll_btn': None,
            'scan_pll_btn': None,
            'tts_tth_btn': None,
            'ini_btn': None,
            'trstat_btn': None,
        }

        self.show()

    def break_thread(self):
        if self.worker is not None:
            self.worker.stop()

    def update_args(self, button_name):
        """Update `args` before running `run_func`."""

        match button_name:
            case 'pedestal_btn':
                self.current_args['pedestal_btn'] = {
                    'fecard': self.fe_card,
                    'data_filter': True,
                    'link': self.__link,
                }
            case 'gain_cross_odd_btn':
                self.current_args['gain_cross_odd_btn'] = {
                    'fecard': self.fe_card,
                    'gen': self.gen,
                    'data_filter': True,
                    'link': self.__link,
                    'parity': 'odd'
                }
            case 'gain_cross_even_btn':
                self.current_args['gain_cross_even_btn'] = {
                    'fecard': self.fe_card,
                    'gen': self.gen,
                    'data_filter': True,
                    'link': self.__link,
                    'parity': 'even'
                }
            case 'raw_btn':
                self.current_args['raw_btn'] = {
                    'fecard': self.fe_card,
                    'runs_number': self.__raw_runs,
                    'data_filter': True,
                    'link': self.__link,
                }
            case 'ttok_btn':
                self.current_args['ttok_btn'] = {
                    'fecard': self.fe_card,
                    'command': self.ttok_lineEdit.text(),
                }
            case 'adcd_btn':
                self.current_args['adcd_btn'] = {
                    'fecard': self.fe_card,
                    'link': self.__link,
                    'n': self.adcd_number_spinBox.value(),
                }
            case 'set_pll_btn':
                self.current_args['set_pll_btn'] = {
                    'fecard': self.fe_card,
                    'link': self.__link,
                    'sh0': self.set_sh0_spinbox.value(),
                    'sh1': self.set_sh1_spinbox.value(),
                }
            case 'scan_pll_btn':
                self.current_args['scan_pll_btn'] = {
                    'fecard': self.fe_card,
                    'link': self.__link,
                    'runs': self.__scan_pll_runs,
                }
            case 'tts_tth_btn':
                self.current_args['tts_tth_btn'] = {
                    'fecard': self.fe_card,
                    'link': self.__link,
                }
            case 'ini_btn':
                self.current_args['ini_btn'] = {
                    'fecard': self.fe_card,
                    'link': self.__link,
                }
            case 'trstat_btn':
                self.current_args['trstat_btn'] = {
                    'fecard': self.fe_card,
                    'link': self.__link,
                }

    def on_button_clicked(self):
        sender = self.sender()
        button_name = sender.objectName()
        if button_name not in self.button_functions:
            print(f'Error: There is no function for {button_name}!')
            return

        self.update_args(button_name)

        run_func = self.button_functions[button_name]
        kwargs = self.current_args[button_name]

        for btn in self.buttonGroup.buttons():
            btn.setEnabled(False)
        sender.setStyleSheet("background-color: red")
        self.stop_thread_btn.setEnabled(True)

        self.execute(button_name=button_name, run_func=run_func, **kwargs)
        # self.stop_thread_btn.setEnabled(False)


    def open_connection_widget(self):
        self.connection_widget = ConnectionForm(self.fe_card, self.gen)
        self.connection_widget.connections_ready.connect(self.handle_connections)
        self.connection_widget.exec()

    def handle_connections(self, fec: FEC, gen: AFG3152C):
        self.fe_card = fec
        self.gen = gen
        for button in self.buttonGroup.buttons():
            button.setEnabled(True)

    def execute(self, *args, **kwargs):
        print(kwargs['run_func'])

        self.worker = Worker(*args, **kwargs)
        self.worker.signals.finished.connect(self.onTelnetFinished)
        self.worker.signals.broken.connect(self.onTelnetBroken)
        self.worker.signals.end.connect(self.onTelnetEnd)
        # Execute
        self.threadpool.start(self.worker)

    @Slot(object)
    def onTelnetEnd(self, button_name):
        print(f'{button_name} is broken!')
        self.stop_thread_flag = False
        self.stop_thread_btn.setEnabled(False)
        for button in self.buttonGroup.buttons():
            button.setEnabled(True)
            # print(f'{button.objectName()=}, {button_name=}')
            if button.objectName() == button_name:
                button.setStyleSheet("")


    @Slot()
    def onTelnetBroken(self):
        self.stop_thread_flag = True


    @Slot(object, object, object, object)
    def onTelnetFinished(self, fec_func, button_name, result, *args, **kwargs):
        print(f'{fec_func.__name__} on {button_name} is finished\n')
        # print(f'{args=}, {kwargs=}')
        self.stop_thread_btn.setEnabled(False)
        for button in self.buttonGroup.buttons():
            button.setEnabled(True)
            if button.objectName() == button_name:
                button.setStyleSheet("")
        match button_name:
            case 'pedestal_btn':
                file_number = self.get_file_number(TestsName.RMS_PEDESTAL)
                vatfilename = f'{file_number}-{self.__card_number}.vat'
                filename = f'{file_number}-{self.__card_number}.txt'
                path = self.get_path(test_name=TestsName.RMS_PEDESTAL)
                path.mkdir(parents=True, exist_ok=True)
                fullpath = Path(path, filename)
                vatfullpath = Path(path, vatfilename)
                header = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0',
                          'Tsam', 'Va2_1_25', 'mA3_S1', 'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']
                np.savetxt(vatfullpath, result['adcd'], delimiter=' ', fmt='%.2f', header=f'{' '.join(header)}')
                with open(fullpath, 'w') as f:
                    for line in result['ff']:
                        f.write((b' '.join(b'0x' + word for word in line) + b'\n').decode())

                self.pedestal_lastrun_label.setText(f'{fullpath}')
                self.plot_run_number_lineEdit.setText(str(file_number))
                self.plot_test_name_comboBox.setCurrentIndex(self.plot_test_name_comboBox.findText('rms_pedestal'))

            case 'gain_cross_odd_btn' | 'gain_cross_even_btn':
                ampl_range = np.concatenate([np.linspace(0.02, 0.1, 9),
                                             np.linspace(0.15, 0.4, 6),
                                             np.linspace(0.45, 0.6, 16),
                                             [2, ]])
                file_number = self.get_file_number(TestsName.GAIN)
                vatfilename = f'{file_number}-{self.__card_number}-2pF.vat'
                path = self.get_path(test_name=TestsName.GAIN)
                vatfullpath = Path(path, vatfilename)
                header = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0',
                          'Tsam', 'Va2_1_25', 'mA3_S1', 'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']
                np.savetxt(vatfullpath, result['adcd'], delimiter=' ', fmt='%.2f', header=f'{' '.join(header)}')
                for ampl in range(len(ampl_range)):

                    filename = f'{file_number}-{self.__card_number}-{args[0]['parity']}-2pF-{round(ampl_range[ampl], 2)}V.txt'
                    fullpath = Path(path, filename)
                    fullpath.parent.mkdir(parents=True, exist_ok=True)
                    with open(fullpath, 'w') as f:
                        for line in result['ff'][ampl]:
                            f.write((b' '.join(b'0x' + word for word in line) + b'\n').decode())
                    self.plot_parity_comboBox.setCurrentText(args[0]['parity'])
                    self.gain_lastrun_label.setText(f'{fullpath}')
                    self.plot_run_number_lineEdit.setText(str(file_number))
                    self.plot_test_name_comboBox.setCurrentIndex(self.plot_test_name_comboBox.findText('gain'))
            case 'raw_btn':
                file_number = self.get_file_number(TestsName.RAW)
                vatfilename = f'{file_number}-{self.__card_number}.vat'
                filename = f'{file_number}-{self.__card_number}.txt'
                path = self.get_path(test_name=TestsName.RAW)
                path.mkdir(parents=True, exist_ok=True)
                fullpath = Path(path, filename)
                vatfullpath = Path(path, vatfilename)
                header = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0',
                          'Tsam', 'Va2_1_25', 'mA3_S1', 'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']
                np.savetxt(vatfullpath, result['adcd'], delimiter=' ', fmt='%.2f', header=f'{' '.join(header)}')
                with open(fullpath, 'w') as f:
                    for line in result['ff']:
                        f.write((b' '.join(b'0x' + word for word in line) + b'\n').decode())

                self.raw_lastrun_label.setText(f'{fullpath}')
                self.plot_run_number_lineEdit.setText(str(file_number))
                self.plot_test_name_comboBox.setCurrentIndex(self.plot_test_name_comboBox.findText('raw'))

            case 'ttok_btn':
                pass
            case 'adcd_btn':
                pass
            case 'set_pll_btn':
                self.tts_tth_led.setColor(QColor('green')) \
                    if result else self.tts_tth_led.setColor(QColor('red'))

            case 'scan_pll_btn':
                card_number = get_card_number(link=self.__link)
                file_number = self.get_file_number(test_name=TestsName.PLL)
                with open(Path(f'{self.get_path(TestsName.PLL)}', f'{file_number}-{card_number}.pll'), 'a') as pf:
                    for i in result:
                        pf.write(str(i) + '\n')
                        print(i)
                self.sh0_value_label.setText(result[0]['sh0'])
                self.sh1_value_label.setText(result[0]['sh1'])
                self.tts_tth_led.setColor(QColor('red'))

            case 'tts_tth_btn':
                self.tts_tth_led.setColor(QColor('green')) \
                    if result else self.tts_tth_led.setColor(QColor('red'))
            case 'ini_btn':
                pass

            case 'trstat_btn':
                with open(Path(DATA_DIR, 'current_fec_trstats.json'), 'r') as f:
                    data = json.load(f)
                    self.__card_number = data['card']
                    pll = dict({'sh0': str(data['sh0']), 'sh1': str(data['sh1'])})
                    self.__pll = pll['sh0'] + ', ' + pll['sh1']
                    self.__cid = data['cid']
                    self.__rid = data['rid']
                    self.__mask = data['mask']
                    self.set_sh1_spinbox.setValue(int(pll['sh1']))
                    self.set_sh0_spinbox.setValue(int(pll['sh0']))

                    self.card_number_value_label.setText(str(self.__card_number))
                    self.pll_value_label.setText(str(self.__pll))
                    self.cid_value_label.setText(str(self.__cid))
                    self.rid_value_label.setText(str(self.__rid))
                    self.mask_value_label.setText(str(self.__mask))
                    self.plot_card_firmware_lineEdit.setText(str(self.__cid))
                    if self.__card_number == 0:
                        self.trstat_led.setColor(QColor('red'))
                    else:
                        self.trstat_led.setColor(QColor('green'))
                    self.plot_card_number_lineEdit.setText(str(self.__card_number))
                    # self.__plot_card_number = self.__card_number
                path = self.get_path(test_name=TestsName.PLL)
                fullname = Path(path, f'{self.__card_number}_in_memory_pll.json')
                path.mkdir(parents=True, exist_ok=True)
                with open(fullname, 'w') as f:
                    json.dump(pll, f)
            case _:
                raise ValueError(f'{fec_func.__name__} is not appropriate')

    def get_path(self, test_name: TestsName = TestsName.RAW) -> Path:
        return Path(RUNS_DIR, f'{self.__card_number}', f'{self.__enc_cdet}', f'{test_name.value}')

    def get_file_number(self, test_name: TestsName = TestsName.RAW) -> int:
        path = self.get_path(test_name)
        path.mkdir(parents=True, exist_ok=True)
        numfile = len(list(path.glob('*.txt')))
        match test_name.value:
            case TestsName.PLL.value:
                return numfile + 1
            case TestsName.RAW.value | TestsName.RMS_PEDESTAL.value:
                return numfile + 1
            case TestsName.GAIN.value:
                return int(-(numfile // -32)) + 1 if numfile else 1  # 25 - len(input amplitudes)
            # case TestsName.CROSSTALK.value:
            #     return int(-(numfile // -2)) + 1 if numfile else 1  # 2 for odd and even
            case _:
                raise ValueError(f'{test_name.value} is not in TestsName')

    def rms_pedestal_fc(self, fecard, link: int = 31, data_filter: bool = True):
        runs_number: int = 100
        self.raw_fc(fecard=fecard, runs_number=runs_number,link=link, data_filter=data_filter)

    def raw_fc(self, fecard, runs_number: int = 10, link: int = 31, data_filter: bool = True):
        adcd = fecard.adcd(n=3, link=link)
        ff = []
        nrun = 1
        while runs_number and not self.stop_thread_flag:
            received_data = fecard.getff(link=link)
            print(f'Run #{nrun}, TTH>>{received_data[-3].decode()}\n')
            data = received_data[1:FW_DATA_LENGTH[f'{self.__cid}'] + 1]
            wform = NWaveForm(data=data, firmware=f'{get_card_fw(link=link)}')
            # print(len(data))
            if not wform.is_valid() and data_filter:
                runs_number += 1
            else:
                ff.append(data)
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
            if self.stop_thread_flag:
                return {'adcd': adcd, 'ff': ff}
            gen.set_volt_low(low=0, channel=gen_channel)
            gen.set_volt_high(high=0.5, channel=gen_channel)
            gen.set_output_state('ON', channel=gen_channel)
            time.sleep(0.1)
            nrun = 1
            ff.append([])
            while runs_number and not self.stop_thread_flag:
                received_data = fecard.getff(link=link)
                print(f'Run #{nrun}, TTH>>{received_data[-3].decode()}\n')
                data = received_data[1:FW_DATA_LENGTH[f'{self.__cid}'] + 1]
                wform = NWaveForm(data=data, firmware=f'{get_card_fw(link=link)}')
                if not wform.is_valid() and data_filter:
                    runs_number += 1
                else:
                    ff[gen_channel - 1].append(data)
                runs_number -= 1
                nrun += 1
            gen.set_output_state('OFF', channel=gen_channel)

        return {'adcd': adcd, 'ff': ff}

    def gain_cross_fc(self, fecard, gen, link: int = 31, parity: str = 'even', data_filter: bool = True):
        adcd = fecard.adcd(n=3, link=link)
        ff = []
        ampl_range = np.concatenate([np.linspace(0.02, 0.1, 9),
                                     np.linspace(0.15, 0.4, 6),
                                     np.linspace(0.45, 0.6, 16),
                                     [2, ]])
        gen_channel = 1 if parity == 'even' else 2
        for ampl in range(len(ampl_range)):
            if self.stop_thread_flag:
                return {'adcd': adcd, 'ff': ff}
            runs_number = 10
            print(f'{ampl=}')
            gen.set_volt_low(low=0, channel=gen_channel)
            gen.set_volt_high(high=round(ampl_range[ampl], 2), channel=gen_channel)
            # gen.set_volt_low(low=0, channel=2)
            # gen.set_volt_high(high=round(ampl_range[ampl], 2), channel=2)
            gen.set_output_state('ON', channel=gen_channel)
            gen.set_output_state('OFF', channel=2 if parity == 'even' else 1)
            time.sleep(0.1)
            ff.append([])
            nrun = 1
            while runs_number and not self.stop_thread_flag:
                received_data = fecard.getff(link=link)
                print(f'Run #{nrun}, TTH>>{received_data[-3].decode()}\n')
                data = received_data[1: FW_DATA_LENGTH[f'{self.__cid}'] + 1]
                wform = NWaveForm(data=data, firmware=f'{get_card_fw(link=link)}')
                if not wform.is_valid() and data_filter:
                    runs_number += 1
                else:
                    ff[ampl].append(data)
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

    def link_value_changed(self):
        self.__link = self.link_spinBox.value()

    def enc_cdet_activate(self, idx):
        self.__enc_cdet = self.enc_cdet_comboBox.itemText(idx)
        self.plot_cdet_comboBox.setCurrentIndex(idx)
        self.__plot_cdet = self.enc_cdet_comboBox.itemText(idx)

    def plot_test_name_handler(self) -> Path:
        match self.plot_test_name_comboBox.currentText():
            case 'rms_pedestal' | 'raw':
                return Path(f'{self.plot_run_number_lineEdit.text()}-{self.plot_card_number_lineEdit.text()}.txt')
            case 'crosstalk':
                return Path(
                    f'{self.plot_run_number_lineEdit.text()}-{self.plot_card_number_lineEdit.text()}-{self.plot_parity_comboBox.currentText()}-2pF.txt')
            case 'gain':
                return Path(
                    f'{self.plot_run_number_lineEdit.text()}-{self.plot_card_number_lineEdit.text()}-{self.plot_parity_comboBox.currentText()}-2pF-{self.plot_amplitude_comboBox.currentText()}V.txt')
            case _:
                raise ValueError(f'No such test: {self.plot_test_name_comboBox.currentText()}')
                # return None

    def update_plots_windows(self):
        filename = self.plot_test_name_handler()
        fullpath = Path(RUNS_DIR,
                        self.plot_card_number_lineEdit.text(),
                        self.plot_cdet_comboBox.currentText(),
                        self.plot_test_name_comboBox.currentText(),
                        filename)
        if fullpath.exists():
            try:
                self.waveform_window.update_plot(filename=fullpath,
                                                 event=int(self.plot_event_number_lineEdit.text()),
                                                 firmware=self.plot_card_firmware_lineEdit.text())
                self.rms_window.update_plot(filename=fullpath,
                                            event=int(self.plot_event_number_lineEdit.text()),
                                            firmware=self.plot_card_firmware_lineEdit.text())
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
            if self.fe_card is not None:
                self.fe_card.tln.write('!\r\n'.encode('utf-8'))
                self.fe_card.tln.close()
                self.gen.close()

            self.waveform_window.close()
            self.rms_window.close()
            print(f'RCU has been closed')
            print(f'GEN has been closed')

            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    try:
        # np.set_printoptions(linewidth=1000, threshold=np.inf)

        app = QApplication(sys.argv)
        w = MainWindow()
        app.exec()
        # print('After EXEC')
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        print(f'Quite')
