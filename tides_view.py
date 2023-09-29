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
        print(f'[0] last - [1] next - [2] next low - [3] lowest next 7 days - [4] next high')
        print(f'[5] highest next 7 days - [6] exit')
        return input('Option: ')

    @staticmethod
    def exit_view() -> None:
        print('Bye!')

    def last_tide_view(self, tide: Tide) -> None:
        print(f'\nLast tide: {tide.state}, '
              f'height: {tide.size_as_float}m, '
              f'when: {datetime.datetime.strftime(tide.datetime_weekly, self.date_formatting_str)}\n')

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

