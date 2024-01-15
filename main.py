import enum
import os
import sys
import telnetlib
from time import perf_counter


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
    # print(f'{result}')
    return result


def transaction(command: str = '2', printing: bool = True) -> bytes:
    if printing:
        print(f'===> <{command}>')
    # write_start = perf_counter()
    tln.write(f'{command}\r\n'.encode('utf-8'))
    # write_stop = perf_counter()
    # print(f'write_time={write_stop - write_start}')
    # result = bytes()
    # read_start = perf_counter()
    received_data: bytes = tln.read_until(b'\r\n')
    # read_stop = perf_counter()
    # print(f'read_time={read_stop - read_start}')
    # if len(received_data) > 0:
    #     result += received_data
    if printing:
        print('Receive >>' + received_data.decode().strip())  # if len(oo)>0:print len(oo),"<",oo,">",
    return received_data


# def ini(link=1, fini=None):
#     power_on(link)
#     if not fini:
#         ttok('wsa 13 30 %d' % link)
#         ttok('wsa 77 30 %d' % link)  # VACFG
#         ttok('wsa 7 30 %d' % link)
#         ttok('wsa 8 0 %d' % link)  # TWLen.0
#         ttok('wsa 71 30 %d' % link)
#         ttok('wsa 72 0 %d' % link)  # TWLen.1
#         ttok('wsa 9 0 %d' % link)
#         ttok('wsa 10 0 %d' % link)
#         ttok('wsa 73 0 %d' % link)
#         ttok('wsa 74 0 %d' % link)  # AQStart
#         ttok('wsa 11 30 %d' % link)
#         ttok('wsa 12 0 %d' % link)
#         ttok('wsa 75 30 %d' % link)
#         ttok('wsa 76 0 %d' % link)  # AQStop
#
#         # w('rsa 7')
#         ttok('wxv 0x944 0x6600 %d' % link)  # # wxv   0x944 0x6600 0;
#
#         ttok('kmsffw 0x0 %d' % link)
#         ttok('kmslkw 0xff %d' % link)  # set k 0;kmsffw 0x0 $k; kmslkw 0x0 $k;
#         ttok('getsetpll %d' % link)
#         return
#
# if fini == 'ini.txt':
#     print
#     " Load from file ..."
#     scri = oscmd("cat ini.txt");
#     lscri = scri.splitlines();
#     for l in lscri:  # цикл по строкам скрипта
#         if l[0] == '#': continue
#         print
#         l[0:len(l) - 2]
#         ttok(l);  # w(';'+l+'\n');
#     # print l
# # print scri


def power_on(link: int = 0):
    powst: bytes = ttok(f'rxv 0x904 {link}').split()[1]
    if powst == b'0x40000003':
        color_print(f'===> SAMPAS power status was = {powst.decode()}', background='b')
        # print 'SAMPAS power status was = %s'%powst;
        print('')
        return
    if powst == b'0x40000001' or powst == b'0x40000002':
        ttok('wxv 0x904 0x3 %d' % link)
        color_print(f'===> New SAMPAS power status = {powst.decode()}', background='y')
        return
    ttok(f'wxv 0x904 0x1 {link}')
    ttok(f'wxv 0x904 0x3 {link}')
    color_print(f'===> New SAMPAS power status = {powst.decode()}', background='g')


def ini(link=1, fini=''):
    power_on(link=link)
    if fini == '':
        ttok(f'wsa 13 30 {link}')
        ttok(f'wsa 77 30 {link}')  # VACFG
        ttok(f'wsa 7 30 {link}')
        ttok(f'wsa 8 0 {link}')  # TWLen.0
        ttok(f'wsa 71 30 {link}')
        ttok(f'wsa 72 0 {link}')  # TWLen.1
        ttok(f'wsa 9 0 {link}')
        ttok(f'wsa 10 0 {link}')
        ttok(f'wsa 73 0 {link}')
        ttok(f'wsa 74 0 {link}')  # AQStart
        ttok(f'wsa 11 30 {link}')
        ttok(f'wsa 12 0 {link}')
        ttok(f'wsa 75 30 {link}')
        ttok(f'wsa 76 0 {link}')  # AQStop

        # w('rsa 7');
        ttok(f'wxv 0x944 0x6600 {link}')  # #  wxv   0x944 0x6600 0;
        ttok(f'kmsffw 0x0 {link}')
        ttok(f'kmslkw 0xff {link}')  # set k 0;kmsffw 0x0 $k; kmslkw 0x0 $k;
        ttok(f'getsetpll {link}')
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


def adc(printing: bool = True):
    result = ttok('adc', printing=printing)
    return result


def adcd(n=10, printing: bool = False):
    # oscmd('echo ".">toConsole.txt');
    #       0       1     2       3      4      5      6      7      8     9      10     11     12     13     14     15
    #    |......|......|......|......|......|......|......|......|......|......|......|......|......|......|......|......|......|
    header = "\n    |  T    1.7Vi  1.1Vc5 1.25Vd mA2 S0 mA1 S0 1.1Vr  1.25Va mA0 S0  Tsam  1.25Va mA3 S1 1.1Vr  mA4 S1 mA5 S1 1.25Va \n"
    global T, Ts
    # oscmd("echo "+ '\"' + "%s"%hd[8:] + '\"' + ">VAT.txt");
    color_print(header)  # print hd
    for j in range(n):
        # if j / 20 * 20 == j:
            # ifstop = oscmd('cat toConsole.txt');
            # if ifstop=='stop\n':
            #     print('stop detected')
            #     break
            # car=ttok('car?;',0);lcar=car.split(' '); print lcar[0]+lcar[1],;
        res = adc(printing=printing)
        ar = res.split(b',')
        if len(ar) < 16:
            print("Wrong length %d" % len(ar))
            break
        if 0 == 0:
            r = 0.61 * int(ar[0], 16)
            a = -1.064200E-09
            b = -5.759725E-06
            c = -1.789883E-01
            d = 2.048570E+02  # set v int*0.61;
            rs = 0.61 * int(ar[9], 16)
            T = a * r ** 3 + b * r ** 2 + c * r + d
            sT = "%2.1f" % T
            Ts = a * rs ** 3 + b * rs ** 2 + c * rs + d
            sTs = "%2.1f" % Ts
            v1 = 0.61 * int(ar[1], 16)
            sv1 = "%2.1f" % v1
            vn = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
            svn = vn
            for k in [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15]:
                vn[k] = 0.61 * int(ar[k], 16)
                svn[k] = "%2.1f" % vn[k]
            #            0    1  2  3   4  5  6  7  8    9

            sout = '      %s  %s %s %s  %s  %s %s %s  %s  %s  %s %s  %s %s  %s  %s ' % \
                   (sT, svn[1], svn[2], svn[3], svn[4], svn[5], svn[6], svn[7], svn[8], sTs, svn[10], svn[11], svn[12],
                    svn[13], svn[14], svn[15])
            print(sout)
            # oscmd("echo " + '\"%s\"' % sout + ">>VAT.txt");
        # print 's: ',res[0:len(res)-2];
        #
        # oscmd('sleep 0.1');


def filn():
    return 44
    # return oscmd('cat filenum.txt')


def carn():
    return 33
    # return oscmd('cat cardname.txt');

class SampaNumber(enum.Enum):
    ZERO: int = 0
    FIRST: int = 1


# def wr(sampa_number: SampaNumber = SampaNumber.ZERO.value):
#     tln.write(f'ttok ;getdd {sampa_number.value}\r\n'.encode('utf-8'))
#
#
# def ru(to=105):
#     result = tln.read_until(b'5555aaaa', to)
#     return result


# def carfil(cn='',fn=0):
#     global carN
#     global filN
#     if cn=='' and fn==0:
#         carN='286';oscmd('echo '+carN+'>cardname.txt')
#         fn=1;oscmd('echo '+'\"'+"%d"%fn+'\"'  + '>filenum.txt')
#     return carN,filN


def getffw(runs_number=1):
    file_number = int(filn())+1
    # ddmon = 'home/serg/pyt/tmp'
    print(f'Initiated run')
    print(f'File name of run {file_number}')
    # oscmd('echo 00 >/home/serg/pyt/tmp/everdy.txt');
    # x = oscmd('cat /home/serg/pyt/tmp/everdy.txt');
    # print ' See /home/serg/tmp/everdy.txt :<%s> '%x;
    with open('events.lst', 'w') as events_file:
        # oscmd('echo ".">toConsole.txt')
        for run in range(runs_number):
            # oscmd('echo 00 >/home/serg/pyt/tmp/everdy.txt')
            # receive_tth = ttok("tth 1", printing=False)
            # print(f'Run #{run+1}, TTH>>{receive_tth.decode()}')
            received_data = ttok(f'tth 1;getdd {SampaNumber.ZERO.value};getdd {SampaNumber.FIRST.value}', False).split(b',')
            print(f'Run #{run+1}, TTH>>{received_data[-3].decode()}')
            # result_list: list = [b'0x' + word for word in received_data[1:-34]]
            # result_string = b' '.join(result_list) + b'\n'
            # fo.write(result_string.decode())
            events_file.write((b' '.join(b'0x' + word for word in received_data[1:-34]) + b'\n').decode())
    fn = f'{int(carn())}-{file_number}.txt'
    oscmd(f'cp events.lst ./{fn}')  ### runs
        # oscmd('cp events.lst ./runs/%s' % fn)  ### runs
        #x = oscmd('cat /home/serg/pyt/tmp/everdy.txt');
        #print ' See /home/serg/tmp/everdy.txt :<%s> '%x;
        #oscmd('cp events.lst /tmp/event.txt');
        #oscmd('echo 0%d>/tmp/everdy.txt'%n);

    return


main_start = perf_counter()

host = '192.168.1.235'
port = 30
tln = telnetlib.Telnet()
tln.open(host=host, port=port)
op1_start = perf_counter()
out = tln.read_until('return:\n\r'.encode('utf-8'))
op1_stop = perf_counter()
print(f'{op1_stop-op1_start=}')
print(out.decode('utf-8'))

# for link in range(3):
#     ttok(f'car {link}')
#     ttok('trstat')
#     ttok('tth 1')
#     ini(link=link)
#     ttok('tth 1')
#     adcd(5)

# sleep(2)
link_n = 1
ttok(';')
ttok(f'car {link_n}')
# ini(link=link_n)
# ttok(f'tth 1')
# adcd(2)
getffw(3)


# ttok()

tln.write('!\r\n'.encode('utf-8'))
tln.close()
main_stop = perf_counter()
print(f'main={main_stop-main_start}')

