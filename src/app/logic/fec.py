import datetime
import enum
import json
import os
import re
import sys
import telnetlib
import time
import traceback
from pathlib import Path
from time import perf_counter

import numpy as np

from app.config import DATA_DIR, RUNS_DIR, TEMP_DIR
from app.logic.data_structure.factory import NWaveForm
from app.logic.slow_control import SlowControl


class BankNumber(enum.Enum):
    ZERO: int = 0
    FIRST: int = 1


class TestsName(enum.Enum):
    # CROSSTALK: str = 'crosstalk'
    # ENC: str = 'enc'
    GAIN: str = 'gain'
    PLL: str = 'pll'
    RAW: str = 'raw'
    RMS_PEDESTAL: str = 'rms_pedestal'


def color_print(message: str, font: str = 'w', background: str = 'd'):
    '''
    Печать символа или строки в цвете без перевода строки.
    Например: pp('111')               - белый на черном
              pp('111',f='y')         - желтый на черном
              pp('111',f='y',b='r')   - желтый на красном
    '''
    xfg = {'d': '30', 'r': '31', 'g': '32', 'y': '33', 'b': '34', 'm': '35', 'c': '36', 'w': '37'}
    xbg = {'d': '40', 'r': '41', 'g': '42', 'y': '43', 'b': '44', 'm': '45', 'c': '46', 'w': '47'}
    cstr = "\033[" + xfg[font] + ';1;' + xbg[background] + 'm' + message + "\033[0m"
    sys.stdout.write(cstr)


def oscmd(cmd):
    pro = os.popen(cmd)
    ret = pro.read()
    pro.close()
    return ret


def get_card_pll(link: int, single: bool = True) -> tuple:
    link = str(link)
    if single:
        with open(Path(DATA_DIR, 'current_fec_trstats.json'), 'r') as f:
            data = json.load(f)
            return data['sh0'], data['sh1']
    else:
        with open(Path(DATA_DIR, 'roc_link_map.json'), 'r') as f:
            data = json.load(f)
            return data[link]['sh0'], data[link]['sh1']


def get_card_fw(link: int = 0, single: bool = True) -> str:
    if single:
        with open(Path(DATA_DIR, 'current_fec_trstats.json'), 'r') as f:
            data = json.load(f)
            return data['cid']
    else:
        with open(Path(DATA_DIR, 'roc_link_map.json'), 'r') as f:
            link = str(link)
            data = json.load(f)
            return data[link]['cid']


def get_card_number(link: int = 0, single: bool = True) -> int:
    if single:
        with open(Path(DATA_DIR, 'current_fec_trstats.json'), 'r') as f:
            data = json.load(f)
            return data['card']
    else:
        with open(Path(DATA_DIR, 'roc_link_map.json'), 'r') as f:
            link = str(link)
            data = json.load(f)
            return data[link]['card']


def get_path(card_number, enc_cdet='0pF', test_name: TestsName = TestsName.RAW) -> Path:
    return Path(RUNS_DIR, f'{card_number}', f'{enc_cdet}', f'{test_name.value}')


def get_file_number(card_number: int, enc_cdet='0pF', test_name: TestsName = TestsName.RAW) -> int:
    path = get_path(card_number, enc_cdet, test_name)
    path.mkdir(parents=True, exist_ok=True)
    numfile = len(list(path.glob('*.txt')))
    match test_name.value:
        case TestsName.PLL.value:
            return numfile + 1
        case TestsName.RAW.value | TestsName.RMS_PEDESTAL.value:
            return numfile + 1
        case TestsName.GAIN.value:
            return int(-(numfile // -32)) + 1 if numfile else 1  # 25 - len(input amplitudes)
        # case TestsName.CROSSTALK.value:
        #     return int(-(numfile // -2)) + 1 if numfile else 1  # 2 for odd and even
        case _:
            raise ValueError(f'{test_name.value} is not in TestsName')


class FEC:
    def __new__(cls, host='192.168.1.235', port=30):
        try:
            instance = super().__new__(cls)
            instance.tln = telnetlib.Telnet(timeout=10)
            instance.tln.open(host=host, port=port)
            print(instance.tln.read_until('return:\n\r'.encode('utf-8')).decode('utf-8'))
            return instance
        except OSError as e:
            print(f'{e}')
            return None

    def __init__(self, host='192.168.1.235', port=30):
        self.__host = host
        self.__port = port

    def ttok(self, command: str, printing: bool = True) -> bytes:
        result = self.transaction(f'ttok ;{command};', printing=printing)
        if printing:
            print(f'==> ttok ;{command}; done\n')
        return result

    def transaction(self, command: str = '2', printing: bool = True) -> bytes:
        if printing:
            print(f'===> <{command}>')
        # write_start = perf_counter()
        self.tln.write(f'{command}\r\n'.encode('utf-8'))
        # write_stop = perf_counter()
        # print(f'write_time={write_stop - write_start}')
        # read_start = perf_counter()
        received_data: bytes = self.tln.read_until(b'\r\n')
        # read_stop = perf_counter()
        # print(f'read_time={read_stop - read_start}')
        if printing:
            print('Receive >>' + received_data.decode().strip())  # if len(oo)>0:print len(oo),"<",oo,">",
        return received_data.strip()

    def power_on(self, link: int = 0) -> None:
        powst_full: bytes = self.ttok(f'rxv 0x904 {link}')
        powst = powst_full.split()[1]
        if powst == b'0x40000003':
            color_print(f'===> SAMPAS power status was = {powst.decode()}', background='b')
            # print 'SAMPAS power status was = %s'%powst;
            print('')
        elif powst == b'0x40000001' or powst == b'0x40000002':
            # ttok(f'wxv 0x904 0x1 {link};wxv 0x904 0x3 {link}')
            self.ttok(f'wxv 0x904 0x3 {link}')
            color_print(f'===> New SAMPAS power status = {powst.decode()}', background='y')
            print('')
        elif powst == b'0x40000000':
            self.ttok(f'wxv 0x904 0x1 {link}')
            time.sleep(1)
            self.ttok(f'wxv 0x904 0x3 {link}')
            # ttok(f'wxv 0x904 0x3 {link}')
            color_print(f'===> New SAMPAS power status = {powst.decode()}', background='g')
            print('')
        else:
            color_print(f'===> SOME ERROR {powst_full.decode()}', background='r')
            print('')

    def check_reg_13_77(self, link: int):
        flag = True
        while flag:
            response = self.ttok(f'wsa 13 30 {link};'
                                 f'wsa 77 30 {link};'
                                 f'rsa 13 {link};'
                                 f'rsa 77 {link}')
            data = response.replace(b' ,', b'').split(b' ') # data=[b'0x4000001e', b'0x4000001e']
            if int(data[0], 16) & 0xff == 30 and int(data[1], 16) & 0xff == 30:
                flag = False
        return True

    def ini(self, link=1, fini=''):
        self.ttok(f'wmsk 0xffffffff;car {link}')
        if fini == '':
            flag = True
            while flag:
                self.power_on(link=link)
                self.check_reg_13_77(link=link)
                self.ttok(
                    # f'wsa 13 30 {link};'
                    # f'wsa 77 30 {link};'  # VACFG
                    f'wsa 7 30 {link};'
                    f'wsa 8 0 {link};'  # TWLen.0
                    f'wsa 71 30 {link};'
                    f'wsa 72 0 {link};'  # TWLen.1
                    f'wsa 9 0 {link};'
                    f'wsa 10 0 {link};'
                    f'wsa 73 0 {link};'
                    f'wsa 74 0 {link};'  # AQStart
                    f'wsa 11 30 {link};'
                    f'wsa 12 0 {link};'
                    f'wsa 75 30 {link};'
                    f'wsa 76 0 {link};'  # AQStop
                    f'wxv 0x944 0x6600 {link};'  # #  wxv   0x944 0x6600 0;
                    f'kmsffw 0x0 {link};'
                    f'kmslkw 0xff {link};'  # set k 0;kmsffw 0x0 $k; kmslkw 0x0 $k;
                    f'getsetpll {link};'
                    f'cff;')
                if 0.0 in self.adcd(link=link, n=1):
                    flag = True
                else:
                    flag = False

        if fini == 'ini.txt':
            print(" Load from file ...")
            scri = oscmd("cat ini.txt")
            lscri = scri.splitlines()
            for line in lscri:  # цикл по строкам скрипта
                if line[0] == '#':
                    continue
                print(line[0:len(line) - 2])
                self.ttok(line)  # w(';'+l+'\n');
                # print l
            # print scri

    def adc(self, link: int = 0, printing: bool = True):
        result = self.ttok(f'wmsk 0xffffffff;car {link};adc', printing=printing)
        return result

    def adcd(self, link: int = 0, n: int = 10, printing: bool = False) -> np.ndarray:
        # oscmd('echo ".">toConsole.txt');
        #       0       1     2       3      4      5      6      7      8     9      10     11     12     13     14     15
        #    |......|......|......|......|......|......|......|......|......|......|......|......|......|......|......|......|......|
        header = "\n    |  T      1.7Vi    1.1Vc5   1.25Vd   mA2_S0   mA1_S0    1.1Vr    1.25Va   mA0_S0    Tsam    1.25Va   mA3_S1   1.1Vr    mA4_S1    mA5_S1   1.25Va \n"
        color_print(header)  # print hd
        # svnarr = np.ndarray(shape=(n, 16))
        svnarr = np.zeros(shape=(n, 16))
        for j in range(n):
            res = self.adc(link=link, printing=printing)
            arow = res.replace(b',', b'').split(b' ')
            ar = [int(a, 16) * 0.61 for a in arow[3:]]
            if 0 == 0:
                r = ar[0]
                a = -1.064200E-09
                b = -5.759725E-06
                c = -1.789883E-01
                d = 2.048570E+02
                rs = ar[9]
                ar[0] = a * r ** 3 + b * r ** 2 + c * r + d
                ar[9] = a * rs ** 3 + b * rs ** 2 + c * rs + d
                ar[4] = float(ar[4]) / 2.5
                ar[5] = float(ar[5]) / 20
                ar[8] = float(ar[8]) / 2.5
                ar[11] = float(ar[11]) / 2.5
                ar[13] = float(ar[13]) / 20
                ar[14] = float(ar[14]) / 2.5
                svn = [val for val in ar]
                # sout = '      %s    %s   %s   %s   %s    %s      %s   %s   %s     %s    %s   %s    %s   %s      %s    %s  ' % \
                #        (svn[0], svn[1], svn[2], svn[3], svn[4], svn[5], svn[6], svn[7], svn[8], svn[9],
                #         svn[10], svn[11], svn[12], svn[13], svn[14], svn[15])
                # print(sout)
                sc = SlowControl(svn)
                data = sc.get_data()
                checked = sc.validate_data(data)
                sc.print_colored_string(checked)

                for idx in range(len(svn)):
                    svnarr[j][idx] = svn[idx]
                # np.vstack([svnarr, [float(s) for s in svn]])

        return svnarr

    def getff(self, link: int, tth: bool = True) -> list[bytes]:
        if tth:
            _tth = 'tth 1;'
        else:
            _tth = ''

        return self.ttok(f'wmsk 0xffffffff;'
                         f'car {link};'
                         f'{_tth}'
                         f'getdd {BankNumber.ZERO.value};'
                         f'getdd {BankNumber.FIRST.value}', False).split(b',')

    def getffw(self, link: int,
               runs_number: int = 1,
               single: bool = False,
               data_filter: bool = True,
               test_name: TestsName = TestsName.RAW,
               tth: bool = True) -> None:
        # ttok(f'car {link}')
        card_number = get_card_number(link=link, single=single)

        path = Path(RUNS_DIR, f'{card_number}', f'0pF', f'{test_name.value}')
        path.mkdir(parents=True, exist_ok=True)

        header = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0',
                  'Tsam', 'Va2_1_25', 'mA3_S1', 'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']

        file_number = int(
            get_file_number(card_number, test_name=test_name))  # TODO придумать как передавать имя теста 1
        file_name = f'{file_number}-{card_number}.txt'
        vatfilename = f'{file_number}-{card_number}.vat'
        vatfullpath = Path(path, vatfilename)

        adcd = self.adcd(n=3, link=link)
        np.savetxt(vatfullpath, adcd, delimiter=' ', fmt='%.2f', header=f'{' '.join(header)}')

        # print(f'Initiated run')
        print(f'Card number: {card_number}, file name: {file_name}, run: {file_number}')
        with open(Path(TEMP_DIR, 'events.lst'), 'w') as events_file:

            nrun = 1
            ff = []
            while runs_number:
                received_data = self.getff(link=link, tth=tth)
                # print(f'{received_data=}')
                # print(f'{len(received_data)=}')
                print(f'Run #{nrun}, TTH>>{received_data[-3].decode()}\n')
                data = received_data[1:779]

                wform = NWaveForm(data=data, firmware=get_card_fw(link=link))
                if not wform.is_valid() and data_filter:
                    runs_number += 1
                else:
                    ff.append(data)
                runs_number -= 1
                nrun += 1

        with open(Path(path, file_name), 'w') as f:
            for line in ff:
                f.write((b' '.join(b'0x' + word for word in line) + b'\n').decode())

        return

    def get_trstat(self, link: int) -> dict:
        fec_trstats = {}
        self.ttok(f'wmsk 0xffffffff;car {link}')
        trstat_data = self.ttok(f'trstat {link}').split(b'  ')
        try:
            cid = trstat_data[2].decode().split(' ')[1]
            # print(trstat_data)
            integrator = 3
            while integrator != 0:
                if cid == '0x00000000':
                    trstat_data = self.ttok(f'trstat {link}').split(b'  ')
                    cid = trstat_data[2].decode().split(' ')[1]
                    integrator -= 1
                else:
                    integrator = 0
            fec_trstats.update({
                'stat': trstat_data[0].decode().split(' ')[1],
                'car': int(trstat_data[1].decode().split(' ')[1]),
                'cid': cid,
                'rid': trstat_data[3].decode().split(' ')[1],
                'mask': trstat_data[4].decode().split(' ')[2],
                'card': int(trstat_data[6].decode().split(' ')[1]),
                'sh0': int(trstat_data[7].decode().split(' = ')[1]),
                'sh1': int(trstat_data[8].decode().split(' ')[0])
            })
        except Exception as e:
            print(e)

        with open(Path(DATA_DIR, 'current_fec_trstats.json'), 'w') as f:
            json.dump(fec_trstats, f)
        return fec_trstats

    def get_trstat_all(self) -> dict:
        roc_link_map = {}
        for link in range(31):
            roc_link_map.update({link: self.get_trstat(link)})
        with open(Path(DATA_DIR, 'roc_link_map.json'), 'w') as f:
            json.dump(roc_link_map, f)
        return roc_link_map

    def get_tth_all(self) -> None:
        for i in range(31):
            self.ttok(f'wmsk 0xffffffff;car {i};ttok ;tth 2')

    def get_tts_tth(self, link) -> bool:
        tth_tts = self.ttok(f'wmsk 0xffffffff;car {link};tts 2;tth 2')
        b = re.findall(r'Nerr=\s\d*\s', tth_tts.decode())
        # print(f'{b=}')
        c = [int(''.join(re.findall(r'\d', i))) for i in b]
        return True if 0 <= (c[0] | c[1]) <= 1 else False

    def get_tts_tth_all(self) -> None:
        for i in range(31):
            self.ttok(f'wmsk 0xffffffff;car {i};tts 2;tth 2')

    def ini_all(self) -> None:
        for link in range(31):
            self.ini(link)

    def tth(self, n: int = 1):
        self.ttok(f'tth {n}')

    def getffw_all(self, runs_number: int = 1) -> None:
        # self.ttok(f'tth 1')
        # for i in range(runs_number):
        # self.tth(1)
        for link in range(31):
            self.getffw(link=link, runs_number=100, single=False, data_filter=False, tth=True)

    def power_off_all(self) -> None:
        for link in range(31):
            self.power_off(link)

    def power_off(self, link: int) -> None:
        self.ttok(f'wmsk 0xffffffff;car {link};wxv 0x904 0x0 {link}')

    def power_on_all(self) -> None:
        for link in range(31):
            self.ttok(f'wmsk 0xffffffff;car {link}')
            self.power_on(link=link)

    def scan_card_pll(self, link: int = 0) -> dict:

        self.ttok(f'car {link}')
        pll = self.ttok('scpll0; scpll1').replace(b',', b'').split(b' ')
        pll_dict = dict()
        pll_dict['sh0'] = bin(int(pll[3], 16))
        pll_dict['sh1'] = bin(int(pll[7], 16))
        return pll_dict

    def set_card_pll(self, link: int = 0, sh0: int = 0, sh1: int = 0) -> bool:
        self.ttok(f'car {link};setpll {sh0} {sh1}')
        response = self.ttok(f'car {link};tts 2; tth 2').split(b' ')  # TODO return?
        print(int(response[9]), int(response[18]))
        return True if (int(response[9]) | int(response[18])) <= 1 else False

    def adcd_all_writable(self, part: str, n: int = 1):
        # ACDC ALL WITH WRITING TO FILE
        import pandas as pd
        # wb = openpyxl.Workbook()
        # ws = wb.active
        # ws.title = 'fec temperatures'

        path = Path(DATA_DIR, 'INP_ROC')
        path.mkdir(parents=True, exist_ok=True)

        time_now = datetime.datetime.now()
        try:
            data_dict = dict()
            df = pd.DataFrame()
            header = ['T', '1.7Vi', '1.1Vc5', '1.25Vd', 'mA2_S0', 'mA1_S0', '1.1Vr', '1.25Va', 'mA0_S0', 'Tsam',
                      '1.25Va', 'mA3_S1', '1.1Vr', 'mA4_S1', 'mA5_S1', '1.25Va']

            for i in range(31):
                print(f'Link={i}')
                data_from_link = self.adcd(link=i, n=n)
                # for adcd_line in data:
                data_dict[f'link{i}'] = data_from_link
                # line = [d[0] for d in data] + [d[9] for d in data]
                # line =
                # if i == 0:
                #     ws.append(['fpga' for _ in range(len(data))] + ['sampa' for _ in range(len(data))])
                # ws.append([d for d in data])
            for link, measurements in data_dict.items():
                adcd_df = pd.DataFrame(measurements, columns=header)  # Преобразуем np.ndarray в DataFrame
                adcd_df['link'] = link  # Добавляем столбец с названием датчика
                df = pd.concat([df, adcd_df], ignore_index=True)
            df.to_excel(Path(path, f'{time_now.strftime("%Y-%m-%d_%H-%M-%S")}_{part}.xlsx'), index=False)
        except Exception as e:
            print(e)
        finally:
            print(f'DONE {time_now.strftime("%Y-%m-%d_%H-%M-%S")}')
            # with open(f'{path}/{time_now}.csv', 'ax') as f:
            # wb.save(f'{path}/{str(time_now)}_N.xlsx')
            # wb.close()


if __name__ == "__main__":
    # import openpixel
    main_start = perf_counter()
    host = '192.168.1.235'

    port = 30
    # tln = telnetlib.Telnet(timeout=10)
    # tln.open(host=host, port=port)
    # out = tln.read_until('return:\n\r'.encode('utf-8'), timeout=10)
    # print(out.decode('utf-8'))
    # wide = FEC(host=host, port=port)
    narrow = FEC(host=host, port=port)

    try:
        np.set_printoptions(linewidth=1000, threshold=np.inf)
        link = 4

        # f.ttok(f'wmsk 0xffffffff')
        narrow.get_trstat(link=link)
        # narrow.power_on(link)

        narrow.ini(link=link)
        narrow.adcd(link=link,n=10)
        # narrow.get_tts_tth(link=link)
        # narrow.adcd(link=link, n=3)
        # a = narrow.getff(link=link)
        # print(a)
        # plldict = narrow.scan_card_pll(link=link)
        # narrow.set_card_pll(link=link, sh0=10, sh1=12)
        # narrow.get_tts_tth(link=link)

        # acdc_all_writable()

        # wide.get_trstat_all()
        # wide.ini_all() # TODO need integrator of 3
        # wide.get_tts_tth_all()
        # for link in range(23,37,1):
        # wide.get_trstat(link)
        # wide.ini(link=link)
        # wide.getffw(link=link,runs_number=100)
        # wide.adcd_all_writable(part='W')
        # wide.getffw_all(runs_number=100)
        # wide.ini(link=0)
        # wide.ttok('cff')
        # wide.adcd(link=link,n=3)

        # narrow.get_trstat_all()
        # narrow.ini_all()
        # narrow.get_tts_tth_all()
        # for link in range(23,24,1):
        #     narrow.get_trstat(link=link)
        #     narrow.ini(link=link)
        # narrow.tth(link=link)
        # narrow.adcd_all_writable(part='N')
        # narrow.getffw_all(runs_number=100)
        # narrow.ttok(f'wmsk 0x00000000')
        # narrow.ttok(f'hard')
        # narrow.tth(1)
        # print(narrow.ttok(f'rff '))
        # narrow.ttok(f'car?')

        # narrow.getffw(link=link, runs_number=1, single=False, data_filter=False, tth=False)
        # narrow.getffw(link=link+1, runs_number=1, single=False, data_filter=False, tth=False)

        # narrow.adcd(link=16, n=100)
        # narrow.get_tts_tth(0)

        # for i in range(31):
        #     # wide.adcd(link=i, n=1)
        #     narrow.adcd(link=i, n=1)

        # print(f'{asd=}')

        # print(f.get_tts_tth(link=link))
        # narrow.getffw_all(runs_number=100)
        # for i in range(31):
        #     narrow.get_trstat(link=i)
        # narrow.getffw(link=10, runs_number=100)
    except KeyboardInterrupt:
        # wide.tln.write('!\r\n'.encode('utf-8'))
        # wide.tln.close()
        narrow.tln.write('!\r\n'.encode('utf-8'))
        narrow.tln.close()
    except Exception as e:
        print(e)
        print(traceback.format_exc())

    finally:
        # wide.tln.write('!\r\n'.encode('utf-8'))
        # wide.tln.close()
        narrow.tln.write('!\r\n'.encode('utf-8'))
        narrow.tln.close()
        main_stop = perf_counter()
        print(f'main_time={main_stop - main_start}')
