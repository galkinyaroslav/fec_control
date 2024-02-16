import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLineEdit, \
    QMessageBox, QLabel
from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool
from fec import FEC  # Импорт вашего модуля FEC


class WorkerSignals(QObject):
    finished = Signal(object)


class Worker(QRunnable):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Store constructor arguments (re-used for processing)
        self.args = args
        self.kwargs = kwargs
        self.fec_func = kwargs['fec_func']
        self.kwargs.pop('fec_func')
        # self.command = command
        self.signals = WorkerSignals()
        # print(f'{args=},{kwargs=}')

    @Slot()
    def run(self):
        # result = self.fe_c.ttok(self.command).decode('utf-8')
        result = self.fec_func(*self.args, **self.kwargs)
        print(f'{type(result)=},{result=}')
        self.signals.finished.emit(str(result))

# class TelnetWorker(QObject):
#     finished = Signal(str)
#
#     def __init__(self, fec_instance, command, parent=None):
#         super().__init__(parent)
#         self.fe_card = fec_instance
#         self.command = command
#
#     def run_telnet_command(self):
#         result = self.fe_card.ttok(self.command).decode('utf-8')
#         self.finished.emit(result)


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
        self.button.clicked.connect(lambda: self.execute(fec_func=self.fe_card.get_trstat, link=31))

        self.button2 = QPushButton("Run ini", self)
        # self.button2.setGeometry(50, 100, 150, 50)
        self.button2.clicked.connect(lambda: self.execute(fec_func=self.fe_card.ini, link=31))

        self.button3 = QPushButton("PLL", self)
        # self.button.setGeometry(50, 100, 150, 50)
        self.button3.clicked.connect(lambda: self.execute(fec_func=self.fe_card.scan_card_pll, link=31))

        self.button4 = QPushButton("tth", self)
        # self.button.setGeometry(50, 100, 150, 50)
        self.button4.clicked.connect(lambda: self.execute(fec_func=self.fe_card.get_tts_tth, link=31))

        self.button5 = QPushButton("getff", self)
        # self.button.setGeometry(50, 100, 150, 50)
        self.button5.clicked.connect(lambda: self.execute(fec_func=self.fe_card.getff, link=31))

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

        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)
        self.centralwidget = QWidget()
        self.centralwidget.setLayout(self.layout)
        self.setCentralWidget(self.centralwidget)

    # def start_telnet_thread(self):
    #     if self.telnet_thread is not None and self.telnet_thread.isRunning():
    #         return
    #     command = self.command_line_edit.text()
    #     self.telnet_thread = QThread()
    #     telnet_worker = TelnetWorker(self.fe_card, command)
    #     telnet_worker.moveToThread(self.telnet_thread)
    #     telnet_worker.finished.connect(self.on_telnet_finished)
    #     self.telnet_thread.started.connect(telnet_worker.run_telnet_command)
    #     self.telnet_thread.start()

    def increment(self):
        a = int(self.label.text())
        self.label.setText(f'{a+1}')

    def execute(self, *args, **kwargs):
        # print(kwargs)
        worker = Worker(*args, **kwargs)
        worker.signals.finished.connect(self.on_telnet_finished)
        # Execute
        self.threadpool.start(worker)

    def on_telnet_finished(self, result):
        print("Telnet result:", result)
        self.text_edit.append(result)


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
