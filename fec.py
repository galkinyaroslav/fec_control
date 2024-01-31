import enum
import json
import os
import sys
import telnetlib
import time
import traceback
from time import perf_counter
from waveform import NWaveForm


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


def ttok(command: str, printing: bool = True) -> bytes:
    result = transaction(f'ttok ;{command};', printing=printing)
    if printing:
        print(f'==> ttok ;{command}; done\n')
    return result


def transaction(command: str = '2', printing: bool = True) -> bytes:
    if printing:
        print(f'===> <{command}>')
    # write_start = perf_counter()
    tln.write(f'{command}\r\n'.encode('utf-8'))
    # write_stop = perf_counter()
    # print(f'write_time={write_stop - write_start}')
    # read_start = perf_counter()
    received_data: bytes = tln.read_until(b'\r\n')
    # read_stop = perf_counter()
    # print(f'read_time={read_stop - read_start}')
    if printing:
        print('Receive >>' + received_data.decode().strip())  # if len(oo)>0:print len(oo),"<",oo,">",
    return received_data.strip()


def power_on(link: int = 0) -> None:
    powst_full: bytes = ttok(f'rxv 0x904 {link}')
    powst = powst_full.split()[1]
    if powst == b'0x40000003':
        color_print(f'===> SAMPAS power status was = {powst.decode()}', background='b')
        # print 'SAMPAS power status was = %s'%powst;
        print('')
    elif powst == b'0x40000001' or powst == b'0x40000002':
        # ttok(f'wxv 0x904 0x1 {link};wxv 0x904 0x3 {link}')
        ttok(f'wxv 0x904 0x3 {link}')
        color_print(f'===> New SAMPAS power status = {powst.decode()}', background='y')
    elif powst == b'0x40000000':
        ttok(f'wxv 0x904 0x1 {link}')
        time.sleep(1)
        ttok(f'wxv 0x904 0x3 {link}')
        # ttok(f'wxv 0x904 0x3 {link}')

        color_print(f'===> New SAMPAS power status = {powst.decode()}', background='g')
    else:
        color_print(f'===> SOME ERROR {powst_full.decode()}', background='r')


def ini(link=1, fini=''):
    ttok(f'car {link}')
    power_on(link=link)
    if fini == '':
        ttok(f'wsa 13 30 {link};'
             f'wsa 77 30 {link};'  # VACFG
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
        # # TODO check setpll sp0 sp1:
        # sh0, sh1 = get_card_pll(link)
        # ttok(f'setpll {sh0} {sh1}')
        return
        #
    if fini == 'ini.txt':
        print(" Load from file ...")
        scri = oscmd("cat ini.txt")
        lscri = scri.splitlines()
        for line in lscri:  # цикл по строкам скрипта
            if line[0] == '#':
                continue
            print(line[0:len(line) - 2])
            ttok(line)  # w(';'+l+'\n');
            # print l
        # print scri


def adc(link: int = 0, printing: bool = True):
    result = ttok(f'car {link};adc', printing=printing)
    return result


def adcd(link: int = 0, n: int = 10, printing: bool = False):
    # oscmd('echo ".">toConsole.txt');
    #       0       1     2       3      4      5      6      7      8     9      10     11     12     13     14     15
    #    |......|......|......|......|......|......|......|......|......|......|......|......|......|......|......|......|......|
    header = "\n    |  T    1.7Vi  1.1Vc5 1.25Vd mA2 S0 mA1 S0 1.1Vr  1.25Va mA0 S0  Tsam  1.25Va mA3 S1 1.1Vr  mA4 S1 mA5 S1 1.25Va \n"
    color_print(header)  # print hd
    for j in range(n):
        res = adc(link=link, printing=printing)
        arow = res.replace(b',', b'').split(b' ')
        ar = [int(a, 16)*0.61 for a in arow[2:]]
        if 0 == 0:
            r = ar[0]
            a = -1.064200E-09
            b = -5.759725E-06
            c = -1.789883E-01
            d = 2.048570E+02
            rs = ar[9]
            ar[0] = a * r ** 3 + b * r ** 2 + c * r + d
            ar[9] = a * rs ** 3 + b * rs ** 2 + c * rs + d
            ar[4] = float(ar[4])/2.5
            ar[5] = float(ar[5])/20
            ar[8] = float(ar[8])/2.5
            ar[11] = float(ar[11])/2.5
            ar[13] = float(ar[13])/20
            ar[14] = float(ar[14])/2.5
            svn = ['%2.1f' % val for val in ar]
            sout = '      %s  %s %s %s   %s  %s %s%s  %s  %s  %s %s  %s %s  %s  %s ' % \
                   (svn[0], svn[1], svn[2], svn[3], svn[4], svn[5], svn[6], svn[7], svn[8], svn[9],
                    svn[10], svn[11], svn[12], svn[13], svn[14], svn[15])
            print(sout)


class TestsName(enum.Enum):
    CROSSTALK: str = 'crosstalk'
    ENC: str = 'enc'
    GAIN: str = 'gain'
    PLL: str = 'pll'
    RAW: str = 'raw'
    RMS_PEDESTAL: str = 'rms_pedestal'
    WORKED_CHANNEL: str = 'worked_channel'


def get_file_number(card_number: int, test_name: TestsName = TestsName.RAW) -> int:
    path = f'./runs/{card_number}/{test_name.value}/'
    if not os.path.exists(path):
        os.makedirs(path)
    return len(os.listdir(path)) + 1


def get_card_number(link: int = 0, single: bool = True) -> int:
    if single:
        with open('current_fec_trstats.json', 'r') as f:
            data = json.load(f)
            return data['card']
    else:
        with open('roc_link_map.json', 'r') as f:
            link = str(link)
            data = json.load(f)
            return data[link]['card']


def get_card_pll(link: int, single: bool = True) -> tuple:
    link = str(link)
    if single:
        with open('current_fec_trstats.json', 'r') as f:
            data = json.load(f)
            return data['sh0'], data['sh1']
    else:
        with open('roc_link_map.json', 'r') as f:
            data = json.load(f)
            return data[link]['sh0'], data[link]['sh1']


class SampaNumber(enum.Enum):
    ZERO: int = 0
    FIRST: int = 1


def getffw(link: int, runs_number: int = 1, single: bool = False):
    # ttok(f'car {link}')
    card_number = get_card_number(link=link, single=single)
    file_number = int(get_file_number(card_number))  # TODO придумать как передавать имя теста 1
    file_mane = f'{file_number}-{card_number}.txt'
    print(f'Initiated run')
    print(f'Card number: {card_number}, file name: {file_mane}, run: {file_number}')
    with open('events.lst', 'w') as events_file:
        nrun = 1
        while runs_number:
            received_data = ttok(f'car {link};'
                                 f'tth 1;'
                                 f'getdd {SampaNumber.ZERO.value};'
                                 f'getdd {SampaNumber.FIRST.value}', False).split(b',')
            # print(f'{received_data=}')
            print(f'Run #{nrun}, TTH>>{received_data[-3].decode()}\n')
            wform = NWaveForm(raw_data=received_data[1:-34])
            if not wform.check_data():
                runs_number += 1
            else:
                events_file.write((b' '.join(b'0x' + word for word in received_data[1:-34]) + b'\n').decode())
            runs_number -= 1
            nrun += 1
    oscmd(f'cp events.lst ./runs/{card_number}/{TestsName.RAW.value}/{file_mane}')  # TODO придумать как передавать имя теста 2
    return


def get_trstat(link: int) -> dict:
    fec_trstats = {}
    ttok(f'car {link}')
    trstat_data = ttok(f'trstat {link}').split(b'  ')
    try:
        cid = trstat_data[2].decode().split(' ')[1]
        print(trstat_data)
        integrator = 3
        while integrator != 0:
            if cid == '0x00000000':
                trstat_data = ttok(f'trstat {link}').split(b'  ')
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

    with open('current_fec_trstats.json', 'w') as f:
        json.dump(fec_trstats, f)
    return fec_trstats


def get_trstat_all() -> dict:
    roc_link_map = {}
    for link in range(31):
        roc_link_map.update({link: get_trstat(link)})
    with open('roc_link_map.json', 'w') as f:
        json.dump(roc_link_map, f)
    return roc_link_map


def get_tth_all() -> None:
    for i in range(31):
        ttok(f'car {i};ttok ;tth 2')


def get_tts_tth_all() -> None:
    for i in range(31):
        ttok(f'car {i};tts 2;tth 2')


def ini_all() -> None:
    for link in range(31):
        ini(link)


def getffw_all(runs_number: int = 1) -> None:
    for link in range(31):
        getffw(link=link, runs_number=runs_number, single=False)


def power_off_all() -> None:
    for link in range(31):
        power_off(link)


def power_off(link: int) -> None:
    ttok(f'car {link};wxv 0x904 0x0 {link}')


def power_on_all() -> None:
    for link in range(31):
        ttok(f'car {link}')
        power_on(link=link)


def scan_card_pll(link: int = 0, runs: int = 1) -> dict:
    ttok(f'car {link}')
    get_trstat(link)
    card_number = get_card_number(link)
    file_number = get_file_number(card_number=card_number, test_name=TestsName.PLL)
    for i in range(runs):
        with (open(f'{file_number}-{card_number}.pll', 'a') as pf):
            ttok(f'car {link}')
            pll = ttok('scpll0; scpll1').replace(b',', b'').split(b' ')
            pll_dict = dict()
            pll_dict['sh0'] = bin(int(pll[3], 16))
            pll_dict['sh1'] = bin(int(pll[7], 16))
            pf.write(str(pll_dict)+'\n')
            print(pll_dict)
    return pll_dict


def set_card_pll(link: int = 0, sh0: int = 0, sh1: int = 0) -> bool:
    ttok(f'car {link};setpll {sh0} {sh1}')
    response = ttok(f'car {link};tts 2; tth 2').split(b' ')  # TODO return?
    print(int(response[9]), int(response[18]))
    if int(response[9]) | int(response[18]) <= 1:
        return True
    else:
        return False


if __name__ == "__main__":
    main_start = perf_counter()
    host = '192.168.1.235'
    port = 30
    tln = telnetlib.Telnet()
    tln.open(host=host, port=port)
    out = tln.read_until('return:\n\r'.encode('utf-8'))
    print(out.decode('utf-8'))

    try:
        # get_trstat_all()
        # ini_all()
        # get_tts_tth_all()
        link = 0
        # ttok(f'wmsk 0xffffffff')
        # ttok(f'car 0')
        # # get_trstat(link=link)
        # # ini(link=link)
        # getffw(link=link, runs_number=1, single=True)
        ttok(f'wmsk 0xfffffffe')
        # ttok(f'car {link}')
        get_trstat(link=link)
        # ttok(f'setpll 17 20')
        # ttok(f'car 2')
        # power_on(0)
        # ttok(f'wsa 13 30 {link}'); time.sleep(1)
        # ttok(f'wsa 77 30 {link}'); time.sleep(1)  # VACFG
        # ttok(f'wsa 7 10 {link}'); time.sleep(1)
        # ttok(f'wsa 8 0 {link}'); time.sleep(1)  # TWLen.0
        # ttok(f'wsa 71 10 {link}'); time.sleep(1)
        # ttok(f'wsa 72 0 {link}'); time.sleep(1)  # TWLen.1
        # ttok(f'wsa 9 0 {link}'); time.sleep(1)
        # ttok(f'wsa 10 0 {link}'); time.sleep(1)
        # ttok(f'wsa 73 0 {link}'); time.sleep(1)
        # ttok(f'wsa 74 0 {link}'); time.sleep(1)  # AQStart
        # ttok(f'wsa 11 10 {link}'); time.sleep(1)
        # ttok(f'wsa 12 0 {link}'); time.sleep(1)
        # ttok(f'wsa 75 10 {link}'); time.sleep(1)
        # ttok(f'wsa 76 0 {link}'); time.sleep(1)  # AQStop
        # ttok(f'wxv 0x944 0x6600 {link}'); time.sleep(1)  # #  wxv   0x944 0x6600 0;
        # ttok(f'kmsffw 0x0 {link}'); time.sleep(1)
        # ttok(f'kmslkw 0xff {link}'); time.sleep(1)  # set k 0;kmsffw 0x0 $k; kmslkw 0x0 $k;
        # ttok(f'getsetpll {link}'); time.sleep(1)
        # ttok(f'cff;')
        # ttok(f'tts 1;tth 1')
        # ttok(f'rff')
        # ttok(f'soft 0')
        # ttok(f'hard 0')
        ttok(f'rsa 13;rsa 77')
        ttok(f'rsa 7;rsa 8')
        ttok(f'rsa 71;rsa 72')
        ttok(f'tth 1')
        ttok(f'getdd 0')
        ttok(f'getdd 1')
        # ttok(f'gwtffw')

        # scan_card_pll(link=link, runs=3)

        # ttok(f'car 0; tth 1;')
        # lo = []
        # with open('temp_tth.lst', 'w') as fl:
        #     for i in range(100):
        #         b = ttok(f'getdd 0; getdd 1').split(b',')
        #         lo.append()
        #         fl.write((b' '.join(b'0x' + word for word in lo) + b'\n').decode())

        # b = ttok(f'getdd 0; getdd 1')

        # a = ['0xfffffffe', '0xfffffffd', '0xfffffffb']
        # for i in range(3):
        #     # ttok(f'jtag1')
        #     # ttok(f'rmsk')
        #     ttok(f'wmsk 0xffffffff')
        #     # ttok(f'rmsk')
        #     get_trstat(link=i)
        #     ini(link=i)
        #     # ttok(f'car {i}')
        #     get_trstat(link=i)
        #     adcd(link=i, n=1)
        #
        #     getffw(link=i, runs_number=1)
        # get_trstat(link=31)
        # ini(link=31)
        # ttok(f'car 31;setpll 6 7')
        # ttok(f'car 31;tts 11; tth 111')
        # adcd(link=31, n=3, printing=False)
        # getffw(link=31, runs_number=1)
        # scan_card_pll(link=31)

        # print(get_card_number(single=True))
        # print(get_file_number())

    except Exception as e:
        print(e)
        print(traceback.format_exc())

    finally:
        tln.write('!\r\n'.encode('utf-8'))
        tln.close()
        main_stop = perf_counter()
        print(f'main_time={main_stop - main_start}')

