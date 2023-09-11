from tides_model import TidesModel
from tides_view import TidesView


class TidesController:
    """
    Controller layer
    """
    def __init__(self):
        self._tm = TidesModel()
        self._tv = TidesView()

    def main(self) -> None:
        implemented_options = {'a': self.next_tide,
                               'b': self.next_low_tide,
                               'c': self.next_lowest_tide,
                               'd': self.next_high_tide,
                               'e': self.next_highest_tide,
                               }
        while True:
            chosen_option = self._tv.start_view()
            if chosen_option in implemented_options:
                implemented_options[chosen_option]()
            else:
                self._tv.exit_view()
                break

    def next_tide(self) -> None:
        self._tv.next_tide_view(self._tm.tides_queries.next_tide)

    def next_low_tide(self) -> None:
        self._tv.next_low_tide_view(self._tm.tides_queries.next_low_tide)

    def next_lowest_tide(self) -> None:
        self._tv.next_lowest_tide_view(self._tm.tides_queries.next_lowest_tide)

    def next_high_tide(self) -> None:
        self._tv.next_high_tide_view(self._tm.tides_queries.next_high_tide)

    def next_highest_tide(self) -> None:
        self._tv.next_highest_tide_view(self._tm.tides_queries.next_highest_tide)


if __name__ == '__main__':
    tc = TidesController()
    tc.main()