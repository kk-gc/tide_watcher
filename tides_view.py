from tides_model import Tide
import datetime


class TidesView:
    """
    View layer for implemented functionalities
    """

    date_formatting_str = '%A, %d/%m/%y at %H:%M'

    @staticmethod
    def start_view() -> str:
        print('=' * 65)
        print('Tide Watcher options:')
        print('(a) next tide\t\t\t\t\t(d) next high tide')
        print('(b) next low tide\t\t\t\t(e) highest tide next 7 days')
        print('(c) lowest tide next 7 days\t\t(f) exit')
        return input('Option: ')

    @staticmethod
    def exit_view() -> None:
        print('Bye!')

    def next_tide_view(self, tide: Tide) -> None:
        print(f'\nNext tide: {tide.state}, '
              f'height: {tide.size_as_float}m, '
              f'when: {datetime.datetime.strftime(tide.datetime_weekly, self.date_formatting_str)}\n')

    def next_low_tide_view(self, tide: Tide) -> None:
        print(f'\nNext low tide, '
              f'height: {tide.size_as_float}m, '
              f'when: {datetime.datetime.strftime(tide.datetime_weekly, self.date_formatting_str)}\n')

    def next_lowest_tide_view(self, tide: Tide) -> None:
        print(f'\nLowest tide in the next 7 days, '
              f'height: {tide.size_as_float}m, '
              f'when: {datetime.datetime.strftime(tide.datetime_weekly, self.date_formatting_str)}\n')

    def next_high_tide_view(self, tide: Tide) -> None:
        print(f'\nNext high tide, '
              f'height: {tide.size_as_float}m, '
              f'when: {datetime.datetime.strftime(tide.datetime_weekly, self.date_formatting_str)}\n')

    def next_highest_tide_view(self, tide: Tide) -> None:
        print(f'\nHighest tide in the next 7 days, '
              f'height: {tide.size_as_float}m, '
              f'when: {datetime.datetime.strftime(tide.datetime_weekly, self.date_formatting_str)}\n')

