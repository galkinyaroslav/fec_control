from dataclasses import dataclass
from pathlib import Path
from typing import Type

import numpy as np

from app.logic.data_structure.processor import BaseDataProcessor, FirmwareProcessor0x24040800, FirmwareProcessor0x23040400


class DataProcessorFactory:
    _processors = {}

    @classmethod
    def register_processor(cls, firmware: str, processor_class: Type[BaseDataProcessor]):
        """Регистрирует обработчик для указанной версии прошивки."""
        cls._processors[firmware] = processor_class

    @classmethod
    def get_processor(cls, data, firmware: str, event: int = -1) -> BaseDataProcessor:
        """Возвращает класс обработчика для указанной версии прошивки."""
        processor_class = cls._processors.get(firmware)
        if not processor_class:
            raise ValueError(f"Обработчик для прошивки '{firmware}' не найден.")
        return processor_class(data,firmware,event)

class NWaveForm:
    def __init__(self, data: np.ndarray | Path, firmware: str, event: int = -1):
        # Получаем обработчик для указанной версии прошивки
        self.processor = DataProcessorFactory.get_processor(data, firmware, event)
        # Обрабатываем данные
        self.data = self.processor.get_waveform_data()
        self.is_valid = self.processor.validate
        self.rms = self.processor.get_rms()
        self.max_value = self.processor.get_max_value()



# Register processor in factory
DataProcessorFactory.register_processor("0x24040800", FirmwareProcessor0x24040800)
DataProcessorFactory.register_processor("0x23040400", FirmwareProcessor0x23040400)
DataProcessorFactory.register_processor("0x23040600", FirmwareProcessor0x23040400)

if __name__ == "__main__":
    from app.config import DATA_DIR, RUNS_DIR

    file_path = Path(DATA_DIR, 'new_structure_file.txt')
    # file_path = Path(RUNS_DIR, '292', 'raw', '1-292.txt')

    obj1 = NWaveForm(data=file_path, firmware="0x24040800")
    # print("Обработанные данные (v1):", obj1.data)
    print(obj1.data[0][0])

    print(len(obj1.data[0][0]))
    print(obj1.rms)
    print(obj1.is_valid)

    # obj2 = A(data=file_path, firmware="0x63040400", event=-1)
    # print("Обработанные данные (v2):", obj2.data)
    # print(len(obj2.data[0][0]))
    # print(obj2.rms)
    # print(obj2.is_valid)