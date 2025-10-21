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
        self.data: np.ndarray | None = self.processor.get_waveform_data()
        self.is_valid = self.processor.validate
        self.rms = self.processor.get_rms()
        self.max_value = self.processor.get_max_value()
        self.mean = self.processor.get_mean()



# Register processor in factory
DataProcessorFactory.register_processor("0x24040800", FirmwareProcessor0x24040800)
DataProcessorFactory.register_processor("0x23040400", FirmwareProcessor0x23040400)
DataProcessorFactory.register_processor("0x23040600", FirmwareProcessor0x23040400)

if __name__ == "__main__":
    from app.config import DATA_DIR, RUNS_DIR
    import pandas as pd
    from matplotlib import pyplot as plt
    CARD_NUMBER = 454
    ENC = '0pF'
    TEST_NAME = 'raw'
    RUN_NUMBER = 113
    file_path = Path(f'{RUNS_DIR}/{CARD_NUMBER}/{ENC}/{TEST_NAME}/{RUN_NUMBER}-{CARD_NUMBER}.txt')
    # file_path = Path(RUNS_DIR, '292', 'raw', '1-292.txt')

    obj1 = NWaveForm(data=file_path, firmware="0x23040600")
    # print("Обработанные данные (v1):", obj1.data)

    fig, ax = plt.subplots()

    RUN_NUMBER = 100
    file_path = Path(f'{RUNS_DIR}/{CARD_NUMBER}/{ENC}/{TEST_NAME}/{RUN_NUMBER}-{CARD_NUMBER}.txt')
    obj2 = NWaveForm(data=file_path, firmware="0x23040600")

    RUN_NUMBER = 92
    file_path = Path(f'{RUNS_DIR}/{CARD_NUMBER}/{ENC}/{TEST_NAME}/{RUN_NUMBER}-{CARD_NUMBER}.txt')
    obj3 = NWaveForm(data=file_path, firmware="0x23040600")

    TEST_NAME = 'rms_pedestal'
    RUN_NUMBER = 1
    file_path = Path(f'{RUNS_DIR}/{CARD_NUMBER}/{ENC}/{TEST_NAME}/{RUN_NUMBER}-{CARD_NUMBER}.txt')
    obj4 = NWaveForm(data=file_path, firmware="0x23040600")

    ax.plot(obj1.rms, 'ro', label='RMS', )
    ax.plot(obj1.rms.mean(), '-r', label='RMS', )
    ax.plot(obj2.rms, 'bo', label='RMS', )
    ax.plot(obj2.rms.mean(), '-b', label='RMS', )
    ax.plot(obj3.rms, 'go', label='RMS', )
    ax.plot(obj3.rms.mean(), 'g-', label='RMS', )
    ax.plot(obj4.rms, 'yo', label='RMS', )
    ax.plot(obj4.rms.mean(), 'y-', label='RMS', )
    print(obj1.rms.mean())
    print(obj2.rms.mean())
    print(obj3.rms.mean())
    print(obj4.rms.mean())
    dic = {'113':obj1.rms,
           '100':obj2.rms,
           '92':obj3.rms,
           '1':obj4.rms,}
    pdf = pd.DataFrame.from_dict(dic, orient='index')
    calculation = Path(f'{RUNS_DIR}/{CARD_NUMBER}/{ENC}/calculations/')
    calculation.mkdir(parents=True, exist_ok=True)
    # pdf_taus.to_excel(Path(f'{RUNS_DIR}/{CARD_NUMBER}/{enc}/calculations/{num}-{CARD_NUMBER}-{enc}-tau.xlsx'))
    # pdf.to_excel(Path(f'{calculation}/{CARD_NUMBER}-rms-collect.xlsx'), index=True)

    plt.show()