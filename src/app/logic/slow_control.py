from pathlib import Path
from colorama import Fore, Style

HEADER = ['T', 'Vi1_7', 'Vc5_1_1', 'Vd1_25', 'mA2_S0', 'mA1_S0', 'Vr1_1_1', 'Va1_1_25', 'mA0_S0', 'Tsam', 'Va2_1_25',
          'mA3_S1', 'Vr2_1_1', 'mA4_S1', 'mA5_S1', 'Va3_1_25']


class SlowControl:
    def __init__(self, raw_data: Path | list) -> None:
        self.raw_data: Path | list = raw_data
        self.__data: dict = {}
        self.__limits: dict = {
            'T': (20, 75),
            'Vi1_7': (1635, 1725),  # +-25
            'Vc5_1_1': (1075, 1125),  # +-25
            'Vd1_25': (1225, 1275),  # +-25
            'mA2_S0': (270, 300),  # +-15
            'mA1_S0': (6, 11),  # +-2.5
            'Vr1_1_1': (1075, 1125),  # +-25
            'Va1_1_25': (1225, 1275),  # +-25
            'mA0_S0': (170, 200),  # +-15
            'Tsam': (20, 75),  # +-25
            'Va2_1_25': (1225, 1275),  # +-25
            'mA3_S1': (170, 200),  # +-15
            'Vr2_1_1': (1075, 1125),  # +-25
            'mA4_S1': (6, 11),  # +-2.5
            'mA5_S1': (270, 300),  # +-15
            'Va3_1_25': (1225, 1275),  # +-25
        }

    @property
    def default_limits(self) -> dict:
        return self.__limits

    def get_data(self) -> dict:
        if isinstance(self.raw_data, Path):
            with open(self.raw_data, 'r') as f:
                f.readline()
                line = f.readline()
                temp_data = [float(val) for val in line.strip().split(' ') if val != '']
                self.__data.update(dict(zip(HEADER, temp_data)))
        elif isinstance(self.raw_data, list):
            self.__data.update(dict(zip(HEADER, self.raw_data)))

        return self.__data

    # @staticmethod
    def validate_data(self, data: dict, limits: dict = None) -> dict:
        """
        Check data against limits

        :param data: data dictionary
        :param limits: limits dictionary {key: (min, max)}
        :return: result dictionary {key: True/False}
        """
        if not limits:
            limits = self.__limits
        result = {}
        for key, value in data.items():
            if key in limits:
                min_val, max_val = limits[key]
                result[key] = min_val <= value <= max_val
            else:
                result[key] = False  # if there is no limit
        return result

    # @staticmethod
    def print_colored_string(self, validation_result, data = None ) -> None:
        """
        Print validation_result equivalent colored string.

        :param validation_result: dictionary {key: (value, True/False)}
        """
        # Make list of strings 'values with colors'
        if not data:
            data = self.__data
        merged_dict = {key: (data[key], validation_result[key]) for key in data}

        colored_values = []
        for key, (value, is_valid) in merged_dict.items():
            color = Fore.RED if not is_valid else Fore.GREEN
            colored_values.append(f'{color}{'%2.1f' % value}{Style.RESET_ALL}')

        # Make and print colored string
        sout = '      %s    %s   %s   %s   %s    %s      %s   %s   %s     %s    %s   %s    %s   %s      %s    %s  ' % \
               (colored_values[0], colored_values[1], colored_values[2], colored_values[3], colored_values[4],
                colored_values[5], colored_values[6], colored_values[7], colored_values[8], colored_values[9],
                colored_values[10], colored_values[11], colored_values[12], colored_values[13], colored_values[14],
                colored_values[15])
        print(sout)


if __name__ == '__main__':
    filename = Path('/home/yaroslav/PycharmProjects/fec_control/src/data/runs_old_to_11_09_24/454/0pF/raw/1-454.vat')
    filename = [47.30, 1616.50, 1095.60, 1240.70, 323.10, 13.90, 1110.20, 1252.90, 223.00, 46.80, 1248.70, 232.30,
                1101.70, 13.50, 316.00, 1247.50
                ]
    sl = SlowControl(filename)
    data = sl.get_data()
    checked = sl.validate_data(data, sl.default_limits)
    print(data)
    print(checked)
    sl.print_colored_string(checked)
