import time
from abc import ABC, abstractmethod
from collections import deque
from itertools import chain
from pathlib import Path

import numpy as np
from app.logic.data_structure import fw_0x64040800


class BaseDataProcessor(ABC):
    def __init__(self, data: list | Path, firmware_version: str, event: int =-1):
        self.firmware_version = firmware_version
        self.data = data
        self.event = event
        self._int_data = self.get_int_data(self.data)
        self._links_data = None
        self._waveform_data = None

    def get_max_value(self):
        return self._waveform_data.max(axis=(0, 2))

    def get_waveform_data(self) -> np.ndarray:
        """compute data"""
        self._waveform_data = self.get_links_data()[:, :, 5:]
        return  self._waveform_data

    def get_rms(self) -> np.array:
        # if self._processed_data is None:
        #     raise ValueError("Data is None")
        return self._waveform_data.std(axis=(0, 2), ddof=1)

    def validate(self) -> bool:
        """Проверяет, соответствуют ли данные условиям"""
        # if self._processed_data is None:
        #     raise ValueError("Data is None")
        condition = self._links_data[:, :, 1] == 31
        return np.all(condition).item()
    @staticmethod
    def get_int(hex_values) -> np.array:
        return [int(value, 16) for value in hex_values]

    def get_int_data(self, data: list | Path) -> np.ndarray:
        data_list = []

        if isinstance(data, Path):
            with open(data, 'r') as file:
                lines = file.readlines()
                print(f'{len(lines)=}')

                match self.event:
                    case -1:
                        for line in lines:
                            hex_values = line.strip().split()
                            decimal_values = self.get_int(hex_values)
                            data_list.append(decimal_values)

                    case x if 0 <= x < len(lines):
                        hex_values = lines[x].strip().split()
                        decimal_values = self.get_int(hex_values)
                        data_list.append(decimal_values)
                    case _:
                        raise ValueError(f'{self.event=} is not appropriate value')
        else:
            data_list = [[int(data, 16) for data in data]]

        return np.array(data_list,)

    def get_links_data(self) -> np.ndarray:
        result_array_3d = np.zeros((self._int_data.shape[0],
                                    self._int_data.shape[1] // 12,
                                    self._int_data.shape[1] // 64 * 3), dtype=np.uint16)
        for i in range(result_array_3d.shape[0]):
            for j in range(result_array_3d.shape[1]):
                for k in range(result_array_3d.shape[2] // 3):
                    val = self._int_data[i, 12 * j + k]
                    d0 = val & 0x3ff
                    d1 = (val >> 10) & 0x3ff
                    d2 = (val >> 20) & 0x3ff
                    result_array_3d[i, j, 3 * k] = d0
                    result_array_3d[i, j, 3 * k + 1] = d1
                    result_array_3d[i, j, 3 * k + 2] = d2
        self._links_data = result_array_3d
        return result_array_3d



class FirmwareProcessor0x24040800(BaseDataProcessor):
    def __init__(self, data, firmware: str, event: int = -1):
        super().__init__(data, firmware, event)
        self._int_data = self.reduce_headers(self._int_data)
        # print(f'{self._int_data=}')

    def reduce_headers(self, data: np.ndarray) -> np.ndarray:
        data_list = []
        for line in range(len(data)):
            link_data_dict: dict = dict()
            link_dict: dict = dict()
            data_deque = deque(data[line])
            # print(len(data_deque))
            card_header_first = fw_0x64040800.CardHeaderFirst(word=data_deque.popleft())
            card_header_second = fw_0x64040800.CardHeaderSecond(word=data_deque.popleft())
            # print(f'{card_header_first=}', card_header_second)
            while len(data_deque) > 0:
                temp = fw_0x64040800.LinkHeader(word=data_deque.popleft())
                # print(temp)
                link = temp.link_number
                link_dict[f'lh{link}'] = temp
                # print(f'{link=}, {link_dict[f'lh{link}'].usedw_n=}')
                # time.sleep(2)
                link_data_dict[f'{link}'] = [data_deque.popleft() for _ in range(link_dict[f'lh{link}'].usedw_n)]
            # print(link_data_dict)
            data_list.append(list(chain.from_iterable(link_data_dict.values())))
            # np_data = np.array([[link_data_dict[f'{lk}'][:, :, 5:]] for lk in range(len(link_data_dict))], dtype=np.uint16)

            # print(f'{len(np_data)=},{np_data=}')
        # for i in data_list:
        #     print(f'{i=}')
        return np.array(data_list)


class FirmwareProcessor0x23040400(BaseDataProcessor):
    def __init__(self, data, firmware: str, event: int = -1):
        super().__init__(data, firmware, event)
        # print(f'{self._int_data=}')
