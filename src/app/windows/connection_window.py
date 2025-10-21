import sys
import traceback

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox, QWidget, QDialogButtonBox

from app.ui.ConnectionWindow_UI import Ui_Dialog


class ConnectionWindow(QWidget, Ui_Dialog):
    def __init__(self, *args, obj=None, **kwargs):
        super(ConnectionWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.rcu_connect_pushButton.clicked.connect(self.connect_to_rcu)
        self.gen_connect_pushButton.clicked.connect(self.connect_to_gen)

        self.buttonBox.accepted.connect(self.accept_dialog)  # OK
        self.buttonBox.rejected.connect(self.reject_dialog)  # Cancel

        # Изначально кнопка OK отключена
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)


        self.fec = None
        self.gen = None

    def connect_to_rcu(self):
        """Connection to RCU logic """
        ip = self.rcu_ip_lineEdit.text()
        port = self.rcu_port_lineEdit.text()
        self.fec = "Соединение с устройством 1 установлено"
        QMessageBox.information(self, "Успех", "Устройство 1 подключено.")
        self.update_ok_button_state()

    def connect_to_gen(self):
        """Connection to GEN logic"""
        # Здесь можно добавить реальную логику подключения
        self.gen = "Соединение с устройством 2 установлено"
        QMessageBox.information(self, "Успех", "Устройство 2 подключено.")
        self.update_ok_button_state()

    def update_ok_button_state(self):
        """Активирует кнопку OK, если оба устройства подключены"""
        if self.connection1 and self.connection2:
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)

    def accept_dialog(self):
        """Обрабатывает нажатие OK"""
        # Передаём соединения в главное окно через сигнал
        self.connections_ready.emit(self.connection1, self.connection2)
        self.accept()  # Закрывает диалог с положительным результатом

    def reject_dialog(self):
        """Обрабатывает нажатие Cancel"""
        self.reject()  # Закрывает диалог с отрицательным результатом


if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        w = ConnectionWindow()
        w.show()
        app.exec()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        print(f'RCU has been closed')