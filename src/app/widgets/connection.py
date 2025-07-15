import json
import sys
import time
import traceback
from pathlib import Path

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QApplication, QMessageBox, QDialogButtonBox, QDialog

from app.logic.fec import FEC
from app.logic.gen import AFG3152C
# from app.logic.waveform import NWaveForm
from app.ui.ConnectionWindow_UI import Ui_Dialog
# from app.logic.workers import Worker
from app.config import DATA_DIR
import jsonschema

SCHEMA = {
    "type": "object",
    "properties": {
        "last_connection": {
            "type": "object",
            "properties": {
                "ip": {"type": "string", "format": "ipv4"},
                "port": {"type": "integer", "minimum": 0, "maximum": 65535}
            },
            "required": ["ip", "port"],
            "additionalProperties": False
        }
    },
    "required": ["last_connection"],
    "additionalProperties": False
}

DEFAULT_IP = '192.168.1.235'
DEFAULT_PORT = '30'
RCU_IP_FILE = 'rcu_ip.json'
class ConnectionForm(QDialog, Ui_Dialog):
    connections_ready = Signal(object, object)

    def __init__(self, fec, gen, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.fec: FEC | None = fec
        self.gen: AFG3152C | None= gen
        print(f'{self.gen=}', f'{self.fec=}')
        if not self.fec and not self.gen:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        # SIGNALS
        self.gen_connect_pushButton.clicked.connect(self.gen_connect)
        self.rcu_connect_pushButton.clicked.connect(self.rcu_connect)
        self.buttonBox.accepted.connect(self.accept_dialog)
        self.buttonBox.rejected.connect(self.reject_dialog)
        self.rcu_ip_lineEdit.editingFinished.connect(self.validate_ip)
        self.rcu_ip_lineEdit.textChanged.connect(self.validate_ip)
        self.rcu_port_lineEdit.editingFinished.connect(self.validate_port)
        self.rcu_port_lineEdit.textChanged.connect(self.validate_port)

        self.rcu_ip_file = Path(DATA_DIR, RCU_IP_FILE)

        if not self.rcu_ip_file.exists():
            # Path.touch(self.rcu_ip_file)  # Создаёт все промежуточные папки
            self.write_json(ip=DEFAULT_IP, port=DEFAULT_PORT)
            print(f'{RCU_IP_FILE} created.')
            self.rcu_ip_lineEdit.setText(DEFAULT_IP)
            self.rcu_port_lineEdit.setText(DEFAULT_PORT)

        else:
            print(f'{RCU_IP_FILE} is already created.')
            with open(self.rcu_ip_file, 'r') as file:
                data = json.load(file)
                # Проверка валидного JSON
                try:
                    jsonschema.validate(instance=data, schema=SCHEMA)
                    print("JSON validated!")
                    self.rcu_ip_lineEdit.setText(data['last_connection']['ip'])
                    self.rcu_port_lineEdit.setText(str(data['last_connection']['port']))
                except jsonschema.exceptions.ValidationError as e:
                    print("Validation Error:", e)
                    self.rcu_ip_lineEdit.setText(DEFAULT_IP)
                    self.rcu_port_lineEdit.setText(str(DEFAULT_PORT))
                    self.write_json(ip=DEFAULT_IP, port=DEFAULT_PORT)

    def write_json(self, ip, port):
        with open(self.rcu_ip_file, 'w') as file:
            file.write(json.dumps({'last_connection': {'ip': ip, 'port': port}}, indent=4))

    @Slot()
    def gen_connect(self):
        """Connection to GEN logic"""
        # Здесь можно добавить реальную логику подключения
        self.gen = AFG3152C()
        if self.gen is not None:
            self.gen.rst()
            time.sleep(1)
            self.gen.set_initial_parameters()
            self.gen_message_received_label.setText('AFG3152C has been connected')
        else:
            self.gen_message_received_label.setText('AFG3152C has NOT been connected')
        self.update_ok_button_state()
    @Slot()
    def rcu_connect(self):
        """Connection to RCU logic """
        ip = self.rcu_ip_lineEdit.text()
        port = self.rcu_port_lineEdit.text()
        self.fec = FEC(host=ip, port=port)
        if self.fec is not None:
            self.rcu_message_received_label.setText('RCU has been connected')
        else:
            self.rcu_message_received_label.setText('RCU has NOT been connected')

        self.update_ok_button_state()

    @Slot()
    def accept_dialog(self):
        """OK"""
        # Передаём соединения в главное окно через сигнал
        self.connections_ready.emit(self.fec, self.gen)
        self.accept()

    @Slot()
    def reject_dialog(self):
        """Cancel"""
        if self.fec is not None:
            self.fec.tln.write('!\r\n'.encode('utf-8'))
            self.fec.tln.close()
        if self.gen is not None:
            self.gen.close()
            # self.fec = None
        self.reject()  # Закрывает диалог с отрицательным результатом

    def update_ok_button_state(self):
        """OK button activation when both devices are connected"""
        if self.fec and self.gen:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    @Slot()
    def validate_ip(self):
        """IP check"""
        ip = self.rcu_ip_lineEdit.text()
        parts = ip.split(".")
        if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
            self.rcu_message_received_label.setText("Valid IP!")
        else:
            QMessageBox.warning(self, "Invalid IP", "Please enter a valid IP address (0-255 in each group).")
            self.rcu_ip_lineEdit.setText(DEFAULT_IP)

    @Slot()
    def validate_port(self):
        """Port check"""
        port = self.rcu_port_lineEdit.text()

        if port.isdigit() and 0 <= int(port) <= 65535:
            self.rcu_message_received_label.setText("Valid Port!")
        else:
            QMessageBox.warning(self, "Invalid Port", "Please enter a port number between 0 and 65535.")
            self.rcu_port_lineEdit.setText(str(DEFAULT_PORT))


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = ConnectionForm()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        print(f'RCU has been closed')
