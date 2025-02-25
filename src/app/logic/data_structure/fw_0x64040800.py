import random
from collections import deque
from dataclasses import dataclass, fields, is_dataclass, field, KW_ONLY
from pathlib import Path

import numpy as np

from app.config import DATA_DIR


@dataclass
class CardHeaderFirst:
    KW_ONLY: KW_ONLY
    AVALON_ADDRESS = 0x94c
    word: int = field(default=None, repr=True)
    header_rg: int = field(default=None, repr=False)

    def __post_init__(self):
        if self.word is not None and self.header_rg is not None:
            raise ValueError("set 'word' or 'header_rg' not both.")

        if self.word is not None:
            self.word = self.word & 0xffffffff  # check 32-bit value
            self.header_rg = self.word & 0x3fffffff
        elif self.header_rg is not None:
            self.header_rg &= 0x3fffffff  # check 30-bit value
            self.word = self.header_rg & 0xffffffff
        else:
            raise ValueError("set at least one of 'word' or 'header_rg'.")

    def __repr__(self):
        return f"CardHeaderFirst(word={self.word:X})"


@dataclass
class CardHeaderSecond:
    KW_ONLY: KW_ONLY
    word: int = field(default=None, repr=True)
    summ_uwd: int = field(default=None, repr=False)
    ef_0: int = field(default=None, repr=False)
    ef_1: int = field(default=None, repr=False)
    ef_2: int = field(default=None, repr=False)
    ef_3: int = field(default=None, repr=False)
    ef_4: int = field(default=None, repr=False)
    ef_5: int = field(default=None, repr=False)
    ef_6: int = field(default=None, repr=False)
    ef_7: int = field(default=None, repr=False)
    ff_0: int = field(default=None, repr=False)
    ff_1: int = field(default=None, repr=False)
    ff_2: int = field(default=None, repr=False)
    ff_3: int = field(default=None, repr=False)
    ff_4: int = field(default=None, repr=False)
    ff_5: int = field(default=None, repr=False)
    ff_6: int = field(default=None, repr=False)
    ff_7: int = field(default=None, repr=False)

    def __post_init__(self):
        if self.word is not None and self.summ_uwd is not None:
            raise ValueError("set 'word' or 'summ_uwd' (with 'ef_n' and 'ff_n') not both.")

        if self.word is not None:
            self.word = self.word & 0xFFFFFFFF  # check 32-bit value
            self.summ_uwd = self.word & 0x3fff
            self.ef_0 = (self.word >> 14) & 1
            self.ef_1 = (self.word >> 15) & 1
            self.ef_2 = (self.word >> 16) & 1
            self.ef_3 = (self.word >> 17) & 1
            self.ef_4 = (self.word >> 18) & 1
            self.ef_5 = (self.word >> 19) & 1
            self.ef_6 = (self.word >> 20) & 1
            self.ef_7 = (self.word >> 21) & 1
            self.ff_0 = (self.word >> 22) & 1
            self.ff_1 = (self.word >> 23) & 1
            self.ff_2 = (self.word >> 24) & 1
            self.ff_3 = (self.word >> 25) & 1
            self.ff_4 = (self.word >> 26) & 1
            self.ff_5 = (self.word >> 27) & 1
            self.ff_6 = (self.word >> 28) & 1
            self.ff_7 = (self.word >> 29) & 1

        elif self.summ_uwd is not None:
            self.summ_uwd &= 0x3FFFF  # check 14-bit value
            self.word = self.summ_uwd & 0xffffffff
            self.word |= (self.ef_0 << 14)
            self.word |= (self.ef_1 << 15)
            self.word |= (self.ef_2 << 16)
            self.word |= (self.ef_3 << 17)
            self.word |= (self.ef_4 << 18)
            self.word |= (self.ef_5 << 19)
            self.word |= (self.ef_6 << 20)
            self.word |= (self.ef_7 << 21)
            self.word |= (self.ff_0 << 22)
            self.word |= (self.ff_1 << 23)
            self.word |= (self.ff_2 << 24)
            self.word |= (self.ff_3 << 25)
            self.word |= (self.ff_4 << 26)
            self.word |= (self.ff_5 << 27)
            self.word |= (self.ff_6 << 28)
            self.word |= (self.ff_7 << 29)
        else:
            raise ValueError("set at lest one of 'word' or 'summ_uwd' (with 'ef_n' and 'ff_n').")

    def __repr__(self):
        return f"CardHeaderSecond(word=0x{self.word:x})"


@dataclass
class LinkHeader:
    KW_ONLY: KW_ONLY
    word: int = field(default=None, repr=True)
    usedw_n: int = field(default=None, repr=False)
    link_number: int = field(default=None, repr=False)

    def __post_init__(self):
        if self.word is not None and self.usedw_n is not None:
            raise ValueError("set 'word' or 'usedw_n' not both.")

        if self.word is not None:
            self.word = self.word & 0xffffffff  # check 32-bit value
            self.usedw_n = self.word & 0x7ff
            self.link_number = (self.word >> 11) & 0x7
        elif self.usedw_n is not None:
            self.usedw_n &= 0x7ff  # check 30-bit value
            self.word = self.usedw_n & 0xffe00000
            self.word |= (self.link_number << 11)
        else:
            raise ValueError("set at least one of 'word' or 'header_rg' (with link_number).")

    def __repr__(self):
        return f"LinkHeader(word=0x{self.word:x})"


def set_bits(word: int, bit_position: int, width: int, new_value: int) -> int:
    # Создаём маску для нужного диапазона битов
    mask = ((1 << width) - 1) << bit_position
    # Сбрасываем биты в нужной позиции и устанавливаем новое значение
    return (word & ~mask) | ((new_value & ((1 << width) - 1)) << bit_position)


def get_int_data(values: list[str]) -> list[int]:
    return [int(i, 16) for i in values]


def get_dec_values(values: list[int]) -> list[int]:
    data = []
    for value in values:
        d0 = value & 0x3ff
        d1 = (value >> 10) & 0x3ff
        d2 = (value >> 20) & 0x3ff
        data.append(d0)
        data.append(d1)
        data.append(d2)
    return data

def generate_32bit_value() -> int:
    part1 = random.randint(0, 1023)  # 10 бит (0–1023)
    part2 = random.randint(0, 1023)  # 10 бит (0–1023)
    part3 = random.randint(0, 1023)  # 10 бит (0–1023)
    value = (part1 << 22) | (part2 << 12) | (part3 << 2)
    return value

def generate_random_list(count):
    return [generate_32bit_value() for _ in range(count)]


def make_event_data(data: list[int]) -> list[str]:
    card_header_first = CardHeaderFirst(word=data[0])
    card_header_second = CardHeaderSecond(word=data[1])
    lh0 = LinkHeader(usedw_n=8 * 12, link_number=0)



    link_data_dict = {f'{a}': data[a * 96:96 * (1 + a)] for a in range(8)}

    lh1 = LinkHeader(usedw_n=8 * 12, link_number=1)
    lh2 = LinkHeader(usedw_n=8 * 12, link_number=2)
    lh3 = LinkHeader(usedw_n=8 * 12, link_number=3)
    lh4 = LinkHeader(usedw_n=8 * 12, link_number=4)
    lh5 = LinkHeader(usedw_n=8 * 12, link_number=5)
    lh6 = LinkHeader(usedw_n=8 * 12, link_number=6)
    lh7 = LinkHeader(usedw_n=8 * 12, link_number=7)
    link_headers_dict = {'0': lh0, '1': lh1, '2': lh2, '3': lh3, '4': lh4, '5': lh5, '6': lh6, '7': lh7}
    summ_uwd = sum(
        [lh0.usedw_n, lh1.usedw_n, lh2.usedw_n, lh3.usedw_n, lh4.usedw_n, lh5.usedw_n, lh6.usedw_n, lh7.usedw_n])
    # card_header_second = CardHeaderSecond(summ_uwd=summ_uwd,
    #                                       ef_0=0,
    #                                       ef_1=0,
    #                                       ef_2=0,
    #                                       ef_3=0,
    #                                       ef_4=0,
    #                                       ef_5=0,
    #                                       ef_6=0,
    #                                       ef_7=0,
    #                                       ff_0=0,
    #                                       ff_1=0,
    #                                       ff_2=0,
    #                                       ff_3=0,
    #                                       ff_4=0,
    #                                       ff_5=0,
    #                                       ff_6=0,
    #                                       ff_7=0)

    int_full_file = []
    for link in range(8):
        if link == 0:
            int_full_file.append(card_header_first.word)
            int_full_file.append(card_header_second.word)
            int_full_file.append(link_headers_dict['0'].word)
            int_full_file.extend(link_data_dict['0'])
            # [int_full_file.append(generate_32bit_value()) for _ in range(link_headers_dict['0'].usedw_n)]
        else:
            int_full_file.append(link_headers_dict[f'{link}'].word)
            int_full_file.extend(link_data_dict[f'{link}'])
            # [int_full_file.append(generate_32bit_value()) for _ in range(link_headers_dict[f'{link}'].usedw_n)]
    hex_full_file = [hex(i) for i in int_full_file]
    # print(f'{len(int_full_file)=} {hex_full_file=}')
    return hex_full_file

def make_fake_event_data(data: list[int]) -> list[str]:

    link_data_dict = {f'{a}': data[a * 96:96 * (1 + a)] for a in range(8)}

    lh0 = LinkHeader(usedw_n=8 * 12, link_number=0)
    lh1 = LinkHeader(usedw_n=8 * 12, link_number=1)
    lh2 = LinkHeader(usedw_n=8 * 12, link_number=2)
    lh3 = LinkHeader(usedw_n=8 * 12, link_number=3)
    lh4 = LinkHeader(usedw_n=8 * 12, link_number=4)
    lh5 = LinkHeader(usedw_n=8 * 12, link_number=5)
    lh6 = LinkHeader(usedw_n=8 * 12, link_number=6)
    lh7 = LinkHeader(usedw_n=8 * 12, link_number=7)
    link_headers_dict = {'0': lh0, '1': lh1, '2': lh2, '3': lh3, '4': lh4, '5': lh5, '6': lh6, '7': lh7}
    summ_uwd = sum(
        [lh0.usedw_n, lh1.usedw_n, lh2.usedw_n, lh3.usedw_n, lh4.usedw_n, lh5.usedw_n, lh6.usedw_n, lh7.usedw_n])
    card_header_first = CardHeaderFirst(word=0x94c)
    card_header_second = CardHeaderSecond(summ_uwd=summ_uwd,
                                          ef_0=0,
                                          ef_1=0,
                                          ef_2=0,
                                          ef_3=0,
                                          ef_4=0,
                                          ef_5=0,
                                          ef_6=0,
                                          ef_7=0,
                                          ff_0=0,
                                          ff_1=0,
                                          ff_2=0,
                                          ff_3=0,
                                          ff_4=0,
                                          ff_5=0,
                                          ff_6=0,
                                          ff_7=0)

    int_full_file = []
    for link in range(8):
        if link == 0:
            int_full_file.append(card_header_first.word)
            int_full_file.append(card_header_second.word)
            int_full_file.append(link_headers_dict['0'].word)
            int_full_file.extend(link_data_dict['0'])
            # [int_full_file.append(generate_32bit_value()) for _ in range(link_headers_dict['0'].usedw_n)]
        else:
            int_full_file.append(link_headers_dict[f'{link}'].word)
            int_full_file.extend(link_data_dict[f'{link}'])
            # [int_full_file.append(generate_32bit_value()) for _ in range(link_headers_dict[f'{link}'].usedw_n)]
    hex_full_file = [hex(i) for i in int_full_file]
    # print(f'{len(int_full_file)=} {hex_full_file=}')
    return hex_full_file

# class FW0x64040800():
#     def __init__(self, full_filename: str = None, raw_data: list[bytes] = None, event: int = -1):
#         self.__event = event
#         if full_filename:
#             self.__full_filename = full_filename
#             self.__raw_data = self.get_raw_data()
#             self.__raw_int_data = self.get_raw_int_data()
#
#
#             self.__all_data = self.convert_data_to_int()
#             self.__waveform_data = self.__all_data[:, :, 5:]
#             self.__rms = self.get_rms()
#         if raw_data:
#             self.__full_filename = None
#             self.__raw_data = raw_data
#             self.__raw_int_data = np.array([[int(data, 16) for data in self.__raw_data]], )
#         self.__all_data = self.convert_data_to_int()
#         self.__waveform_data = self.__all_data[:, :, 5:]
#         self.__rms = self.get_rms()
#         self.__max_value = self.get_max_value()
#         self.n_events = self.__waveform_data.shape[0]
#         with open(test_file_path, 'r') as f:
#             link_data_dict: dict = dict()
#             link_dict: dict = dict()
#             # str_data = f.readline()
#             # print(str_data)
#             data = get_int_data(f.readline().split())
#             print(data)
#     def get_raw_data(self) -> np.ndarray:
#         with open(self.__full_filename, 'r') as file:
#             lines = file.readlines()
#             print(f'{len(lines)=}')
#         match self.__event:
#             case -1:
#                 data_list = []
#                 for line in lines:
#                     hex_values = line.strip().split()
#                     # decimal_values = [int(value, 16) for value in hex_values]
#                     data_list.append(hex_values)
#                 return np.array(data_list)
#
#             case x if 0 <= x < len(lines):
#                 data_list = []
#                 hex_values = lines[x].strip().split()
#                 # decimal_values = [int(value, 16) for value in hex_values]
#                 data_list.append(hex_values)
#                 return np.array(data_list)
#             case _:
#                 raise ValueError(f'{self.__event=} is not appropriate value')
#
#     # def make_fake_event_data(self, data: list[int]) -> list[str]:
#     #
#     #     data_deque = deque(data)
#     #
#     #     self.__card_header_first = data_deque.popleft()
#     #     self.__card_header_second = data_deque.popleft()
#     #
#     #     while len(data_deque) > 0:
#     #         temp = LinkHeader(word=data_deque.popleft())
#     #         link = temp.link_number
#     #         link_dict[f'lh{link}'] = temp
#     #         print(link)
#     #         link_data_dict[f'{link}'] = get_dec_values(
#     #             [data_deque.popleft() for _ in range(link_dict[f'lh{link}'].usedw_n)])
#     #         # print(link_data_dict[f'{link}'])
#     #
#     #         print(f'{len(link_data_dict[f'{link}'])=},{link_data_dict[f'{link}']=}')
#

if __name__ == '__main__':
    test_file_path = Path(DATA_DIR, 'new_structure_file.txt')

    with open(test_file_path, 'r') as f:
        link_data_dict : dict = dict()
        link_dict : dict = dict()
        data = get_int_data(f.readline().split())
        print(data)
        # def make_fake_event_data(data: list[int]) -> list[str]:
        data_deque = deque(data)

        card_header_first = CardHeaderFirst(word=data_deque.popleft())
        card_header_second = CardHeaderSecond(word=data_deque.popleft())
        print(card_header_first.word)
        print(card_header_second.word)


        while len(data_deque)>0:
            temp = LinkHeader(word=data_deque.popleft())
            link = temp.link_number
            link_dict[f'lh{link}'] = temp
            print(f'{link=}, {link_dict[f'lh{link}'].usedw_n=}')
            link_data_dict[f'{link}'] = get_dec_values([data_deque.popleft() for _ in range(link_dict[f'lh{link}'].usedw_n)])
            # link_data_dict[f'{link}'] = get_dec_values([data_deque.popleft() for _ in range(link_dict[f'lh{link}'].usedw_n)])

            print(link_data_dict[f'{link}'])
        np_data = np.array([[link_data_dict[f'{lk}'][:,:,5:]] for lk in range(len(link_data_dict))], dtype=np.uint16)

        print(f'{len(np_data)=},{np_data=}')

        # print(link_dict)
        # print(link_data_dict['0'])
        # print(link_data_dict['1'])


    #     data_raw = f.readline().strip().split()
    #     # print(type(data))
    #     data_int = get_int_data(data_raw)
    #
    #     fake_data = make_fake_event_data(data_int)
    #     print(fake_data)



