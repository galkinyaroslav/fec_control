import keyword
import os
import sys
import time

import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLineEdit, \
    QMessageBox, QLabel
from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool
from fec import FEC  # Импорт вашего модуля FEC
from waveform import NWaveForm


class WorkerSignals(QObject):
    finished = Signal(object, object, object)


class Worker(QRunnable):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.run_func = kwargs['run_func']
        print(f'{type(self.kwargs)}')
        self.kwargs.pop('run_func')
        # self.command = command
        self.signals = WorkerSignals()
        # print(f'{args=},{kwargs=}')

    @Slot()
    def run(self):
        result = self.run_func(*self.args, **self.kwargs)
        self.signals.finished.emit(self.run_func, result, self.kwargs)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.fe_card = FEC()  # Создаем объект FEC при инициализации главного окна
        # self.telnet_thread = None
        self.threadpool = QThreadPool()

    def init_ui(self):
        self.setWindowTitle("Telnet Example")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()
        self.command_line_edit = QLineEdit(self)
        # self.command_line_edit.setGeometry(50, 50, 300, 30)

        self.btn = QPushButton("click")
        self.btn.clicked.connect(self.increment)
        self.label = QLabel(self)
        self.label.setText("0")

        self.button = QPushButton("trstat", self)
        # self.button.setGeometry(50, 100, 150, 50)
        self.button.clicked.connect(lambda: self.execute(run_func=self.fe_card.get_trstat, link=31))

        self.button2 = QPushButton("Run ini", self)
        # self.button2.setGeometry(50, 100, 150, 50)
        self.button2.clicked.connect(lambda: self.execute(run_func=self.fe_card.ini, link=31))

        self.button3 = QPushButton("PLL", self)
        # self.button.setGeometry(50, 100, 150, 50)
        self.button3.clicked.connect(lambda: self.execute(run_func=self.fe_card.scan_card_pll, link=31))

        self.button4 = QPushButton("tth", self)
        # self.button.setGeometry(50, 100, 150, 50)
        self.button4.clicked.connect(lambda: self.execute(run_func=self.fe_card.get_tts_tth, link=31))

        self.button5 = QPushButton("getff", self)
        # self.button.setGeometry(50, 100, 150, 50)
        self.button5.clicked.connect(lambda: self.execute(run_func=self.fe_card.getff, link=31))

        self.button6 = QPushButton("adcd", self)
        # self.button.setGeometry(50, 100, 150, 50)
        self.button6.clicked.connect(lambda: self.execute(run_func=self.fe_card.adcd, n=10, link=31))

        self.button7 = QPushButton('adcd_getff', self)
        self.button7.clicked.connect(lambda: self.execute(run_func=self.adcd_getff,
                                                          fecard=self.fe_card,
                                                          runs_number=2,
                                                          data_filter=False,
                                                          link=31
                                                          ))

        self.text_edit = QTextEdit(self)

        # self.text_edit.setGeometry(50, 170, 300, 100)
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.command_line_edit)

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button4)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button5)
        self.layout.addWidget(self.button6)
        self.layout.addWidget(self.button7)

        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)
        self.centralwidget = QWidget()
        self.centralwidget.setLayout(self.layout)
        self.setCentralWidget(self.centralwidget)

    def adcd_getff(self, fecard, runs_number, data_filter, link):

        adcd = fecard.adcd(n=3, link=link)
        ff = []
        nrun = 1
        while runs_number:
            received_data = fecard.getff(link=link)
            print(f'{received_data=}')
            print(f'Run #{nrun}, TTH>>{received_data[-3].decode()}\n')
            wform = NWaveForm(raw_data=received_data[1:-34])
            if not wform.check_data() and data_filter:
                runs_number += 1
            else:
                ff.append(received_data[1:-34])
            runs_number -= 1
            nrun += 1

        return {'adcd': adcd, 'ff': ff}

    def increment(self):
        a = int(self.label.text())
        self.label.setText(f'{a + 1}')

    def execute(self, *args, **kwargs):
        # print(kwargs)
        worker = Worker(*args, **kwargs)
        worker.signals.finished.connect(self.on_telnet_finished)
        # Execute
        self.threadpool.start(worker)

    @Slot(object, object, object)
    def on_telnet_finished(self, fec_func, result, *args, **kwargs):
        # print("Telnet fec_func:", fec_func)
        print(f'{fec_func.__name__} is finished')
        match fec_func.__name__:
            case 'adcd_getff':
                print(f'{result['adcd']=}')
                print(f'{result["ff"]=}')
                vatfilename = f'test-454.vat'
                filename = f'test-454.txt'

                path = (f'runs/'
                        f'454/'
                        f'0pF/'
                        f'raw/')
                fullpath = path + filename
                vatfullpath = path + vatfilename
                header = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0', 'Tsam',
                          'Va2_1_25', 'mA3_S1', 'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']
                # with open(vatfullpath, 'w') as f:
                #     f.write(f'{' '.join(header)}\n',)
                # time.sleep(10)
                np.savetxt(vatfullpath, result['adcd'], delimiter=' ', fmt='%.2f', header=f'{' '.join(header)}')
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(fullpath, 'w') as f:
                    for line in result['ff']:
                        f.write((b' '.join(b'0x' + word for word in line) + b'\n').decode())
        print("Telnet result:", result)
        print("Telnet args:", args)
        print("Telnet kwargs:", kwargs)
        # self.text_edit.append(result)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.fe_card.tln.write('!\r\n'.encode('utf-8'))
            self.fe_card.tln.close()
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
