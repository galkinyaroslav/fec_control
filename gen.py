import time

import pyvisa
import re


class AFG3152C():
    def __init__(self):
        self.__DEVICE_NAME = 'AFG3152C'
        self.__rm = pyvisa.ResourceManager()  # '/usr/lib/x86_64-linux-gnu/libiovisa.so')
        self.__inst = self.find_inst()

    def find_inst(self):
        list_res = self.__rm.list_resources()
        print(list_res)

        # ('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::12::INSTR')
        devices = [i for i in list_res if 'TCPIP' in i]
        for instrument in devices:
            try:
                temp_device = self.__rm.open_resource(instrument)
                temp_name = temp_device.query("*IDN?")
                if self.__DEVICE_NAME in temp_name:
                    print(temp_name.strip(), '--->>>', instrument)
                    return temp_device
                else:
                    temp_device.close()
            except pyvisa.errors.VisaIOError:
                print('This is not appropriate device or device is not found')

    def rst(self):
        self.__inst.write('*RST')

    def set_function(self, function_name):
        self.__inst.write(f'SOUR1:FUNC:SHAP {function_name}')

    def set_pulse_period(self, period: float = 1, units: str = 'ms'):
        self.__inst.write(f'SOUR1:PULS:PER {period}{units}')

    def set_pulse_width(self, width: float = 1, units: str = 'us'):
        self.__inst.write(f'SOUR1:PULS:WIDT {width}{units}')

    def set_pulse_tran(self, lead: float = 3, trail: int = 3, units: str = 'ns'):
        self.__inst.write(f'SOUR1:PULS:TRAN:TRA {trail}{units}')
        self.__inst.write(f'SOUR1:PULS:TRAN:LEAD {lead}{units}')

    def set_volt_offset(self, offset: float = 0, units: str = 'mV'):
        self.__inst.write(f'SOUR1:VOLT:LEV:IMM:OFFS {offset}{units}')

    def set_volt_amplitude(self, amplitude: int = 10, units: str = 'mV'):
        self.__inst.write(f'SOUR1:VOLT:LEV:IMM:AMPL {amplitude}{units}')

    def get_volt_amplitude(self):
        return self.__inst.query(f'SOUR1:VOLT:LEV:IMM:AMPL?')

    def set_volt_low(self, low: float = 0, units: str = 'mV'):
        self.__inst.write(f'SOUR1:VOLT:LEV:IMM:LOW {low}{units}')

    def set_volt_high(self, high: float = 0, units: str = 'mV'):
        self.__inst.write(f'SOUR1:VOLT:LEV:IMM:HIGH {high}{units}')

    def set_burst_state(self, burst_state: str = 'OFF'):
        self.__inst.write(f'SOUR1:BURS:STATE {burst_state}')

    def set_burst_mode(self, mode: str = 'TRIG'):
        self.__inst.write(f'SOUR1:BURS:MODE {mode}')

    def set_burst_ncycle(self, cycles: int = 1):
        self.__inst.write(f'SOUR1:BURS:NCYC {cycles}')

    def set_burst_triggerdelay(self, tdelay: float = 0, units: str = 'us') -> None:
        self.__inst.write(f'SOUR1:BURS:TDEL {tdelay}{units}')

    def set_trigger_source(self, source: str = 'EXT') -> None:
        self.__inst.write(f'TRIG:SEQ:SOUR {source}')

    def set_output_state(self, state: str = 'OFF') -> None:
        self.__inst.write(f'OUTP1:STAT {state}')

    def set_initial_parameters(self):
        self.rst()
        self.set_function('PULS')

        self.set_pulse_period(period=1, units='ms')
        self.set_pulse_width(width=5, units='us')
        self.set_pulse_tran()


        self.set_volt_low(0)
        self.set_volt_high(200)

        self.set_burst_state('ON')
        self.set_burst_mode('TRIG')
        self.set_burst_ncycle(cycles=1)
        self.set_burst_triggerdelay(tdelay=1.5, units='us')

        # self.set_volt_offset(100)
        # self.set_volt_amplitude(amplitude=150, units='mV')

        self.set_trigger_source('EXT')

        self.set_output_state('ON')


if __name__ == '__main__':

    afg = AFG3152C()
    afg.rst()
    time.sleep(1)
    afg.set_initial_parameters()
    print(afg.get_volt_amplitude())
    # for i in range(100):
    #     afg.set_volt_high(high=i*10)
    #     time.sleep(0.3)
