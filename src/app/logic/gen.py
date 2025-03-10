from typing import Type

import pyvisa


class AFG3152C:
    def __new__(cls):
        instance = super().__new__(cls)
        instance.__rm = pyvisa.ResourceManager()

        instance.__DEVICE_NAME = 'AFG3152C'
        temp = cls.find_inst(rm=instance.__rm, device_name=instance.__DEVICE_NAME)
        if temp is None:
            return None
        instance.__inst = temp
        return instance

    def __init__(self):
        pass
        # self.__DEVICE_NAME = 'AFG3152C'
        # self.__rm = pyvisa.ResourceManager()  # '/usr/lib/x86_64-linux-gnu/libiovisa.so')
        # self.__inst = self.find_inst()

    @property
    def inst(self):
        return self.__inst

    def close(self):
        self.__inst.close()
        self.__rm.close()

    @staticmethod
    def find_inst(rm: pyvisa.ResourceManager, device_name: str) -> pyvisa.resources.Resource | None:
        list_res = rm.list_resources()
        print(list_res)

        # ('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::12::INSTR')
        devices = [i for i in list_res if 'TCPIP' in i]
        for instrument in devices:
            try:
                temp_device = rm.open_resource(instrument)
                temp_name = temp_device.query("*IDN?")
                if device_name in temp_name:
                    print(temp_name.strip(), '--->>>', instrument)
                    return temp_device
                else:
                    temp_device.close()
            except pyvisa.errors.VisaIOError:
                print('This is not appropriate device or device is not found')
        return None


    def rst(self):
        self.__inst.write('*RST')

    def set_function(self, function_name, channel: int = 1):
        self.__inst.write(f'SOUR{channel}:FUNC:SHAP {function_name}')

    def set_pulse_period(self, period: float = 1, units: str = 'ms', channel: int = 1):
        self.__inst.write(f'SOUR{channel}:PULS:PER {period}{units}')

    def set_pulse_width(self, width: float = 1, units: str = 'us', channel: int = 1):
        self.__inst.write(f'SOUR{channel}:PULS:WIDT {width}{units}')

    def set_pulse_tran(self, lead: float = 3, trail: int = 3, units: str = 'ns', channel: int = 1):
        self.__inst.write(f'SOUR{channel}:PULS:TRAN:TRA {trail}{units}')
        self.__inst.write(f'SOUR{channel}:PULS:TRAN:LEAD {lead}{units}')

    def set_volt_offset(self, offset: float = 0, units: str = 'V', channel: int = 1):
        # self.__inst.write(f'SOUR1:VOLT:LEV:IMM:OFFS {offset}{units}')
        self.__inst.write(f'SOUR{channel}:VOLT:OFFS {offset:.3e}')


    def set_volt_amplitude(self, amplitude: int = 10, units: str = 'V', channel: int = 1):
        self.__inst.write(f'SOUR{channel}:VOLT:AMPL {amplitude:.3e}')

    def get_volt_amplitude(self, channel: int = 1):
        return self.__inst.query(f'SOUR{channel}:VOLT:AMPL?')

    def set_volt_low(self, low: float = 0, units: str = 'V', channel: int = 1):
        self.__inst.write(f'SOUR{channel}:VOLT:LOW {low:.3e}')

    def set_volt_high(self, high: float = 0, units: str = 'V', channel: int = 1):
        self.__inst.write(f'SOUR{channel}:VOLT:HIGH {high:.3e}')

    def set_burst_state(self, burst_state: str = 'OFF', channel: int = 1):
        self.__inst.write(f'SOUR{channel}:BURS:STATE {burst_state}')

    def set_burst_mode(self, mode: str = 'TRIG', channel: int = 1):
        self.__inst.write(f'SOUR{channel}:BURS:MODE {mode}')

    def set_burst_ncycle(self, cycles: int = 1, channel: int = 1):
        self.__inst.write(f'SOUR{channel}:BURS:NCYC {cycles}')

    def set_burst_triggerdelay(self, tdelay: float = 0, units: str = 'us', channel: int = 1) -> None:
        self.__inst.write(f'SOUR{channel}:BURS:TDEL {tdelay}{units}')

    def set_trigger_source(self, tsource: str = 'EXT', channel: int = 1) -> None:
        self.__inst.write(f'TRIG:SEQ:SOUR {tsource}')

    def set_output_state(self, state: str = 'OFF', channel: int = 1) -> None:
        self.__inst.write(f'OUTP{channel}:STAT {state}')

    def set_initial_parameters(self):
        self.rst()

        self.set_function('PULS')

        self.set_pulse_period(period=5, units='us')
        self.set_pulse_width(width=4, units='us')
        self.set_pulse_tran(lead=3, trail=3, units='ns')

        self.set_volt_low(0)
        self.set_volt_high(0.2)

        self.set_burst_state('ON')
        self.set_burst_mode('TRIG')
        self.set_burst_ncycle(cycles=1)
        self.set_burst_triggerdelay(tdelay=2, units='us')

        self.set_trigger_source('EXT')

        self.set_output_state('OFF')

        self.set_function('PULS', channel=2)

        self.set_pulse_period(period=5, units='us', channel=2)
        self.set_pulse_width(width=4, units='us', channel=2)
        self.set_pulse_tran(lead=3, trail=3, units='ns', channel=2)

        self.set_volt_low(0, channel=2)
        self.set_volt_high(0.2, channel=2)

        self.set_burst_state('ON', channel=2)
        self.set_burst_mode('TRIG', channel=2)
        self.set_burst_ncycle(cycles=1, channel=2)
        self.set_burst_triggerdelay(tdelay=2, units='us', channel=2)

        self.set_trigger_source('EXT', channel=2)

        self.set_output_state('OFF', channel=2)


if __name__ == '__main__':
    import numpy
    import time

    afg = AFG3152C()
    afg.rst()
    time.sleep(1)
    afg.set_initial_parameters()
    print(afg.get_volt_amplitude())
    afg.set_volt_low(low=0)

    for i in numpy.linspace(0.02, 0.1, 10):
        # afg.set_volt_amplitude(amplitude=i)
        # afg.set_volt_offset(offset=0.04)
        afg.set_volt_high(high=i)
        time.sleep(0.3)
