from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QThread, QObject, Signal
import time
import sys


# 🔹 Главное окно
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Остановка потока")

        # Кнопки управления
        self.start_button = QPushButton("Запустить операцию")
        self.stop_button = QPushButton("Остановить")
        self.stop_button.setEnabled(False)  # По умолчанию отключена

        # Размещение кнопок
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Подключаем сигналы
        self.start_button.clicked.connect(self.start_operation)
        self.stop_button.clicked.connect(self.stop_operation)

    def start_operation(self):
        """Запускаем поток с длительной операцией"""
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.thread = QThread()
        self.worker = Worker(device="MyDevice")  # Передаём устройство
        self.worker.moveToThread(self.thread)

        # Подключаем сигналы
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.on_operation_finished)

        # Остановка потока
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def stop_operation(self):
        """Останавливаем поток"""
        if hasattr(self, "worker"):
            self.worker.stop()  # Устанавливаем флаг остановки

    def update_status(self, message):
        """Обновление статуса (можно добавить QLabel)"""
        print(message)

    def on_operation_finished(self, result):
        """Действия после завершения потока"""
        print(f"🔔 Завершение: {result}")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)  # Отключаем кнопку остановки

# 🔹 Запуск приложения
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
