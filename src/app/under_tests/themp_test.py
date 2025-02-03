import sys
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

class Worker(QObject):
    data_ready = Signal(str)

    @Slot()
    def do_work(self):
        counter = 1
        while True:
            self.data_ready.emit(f"Data {counter}")
            counter += 1
            QThread.msleep(1000)  # Задержка в миллисекундах

class Controller(QObject):
    stop_timer = Signal()

    def __init__(self, worker):
        super().__init__()
        self.worker = worker
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.worker.data_ready.connect(self.handle_data_ready)
        self.stop_timer.connect(self.worker.do_work)

        self.thread.started.connect(self.worker.do_work)

    @Slot(str)
    def handle_data_ready(self, data):
        print(data)  # Здесь можно добавить обработку данных
        with open("../../../temp/output.txt", "a") as f:
            f.write(data + "\n")

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.quit()

def main():
    app = QApplication(sys.argv)

    worker = Worker()
    controller = Controller(worker)

    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)

    start_button = QPushButton("Start")
    stop_button = QPushButton("Stop")

    start_button.clicked.connect(controller.start)
    stop_button.clicked.connect(controller.stop)

    layout.addWidget(start_button)
    layout.addWidget(stop_button)

    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
