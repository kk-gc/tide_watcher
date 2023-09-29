import requests
import datetime
import re
import os


class Scraper:
    """
    scrape data from https://www.tidetime.org/europe/spain/las-palmas-de-gran-canaria.htm

    """
    def __init__(self, location='las-palmas-de-gran-canaria'):
        self.scrape_time = datetime.datetime.today()
        self.location = location
        self.raw_data = self._get_raw_data()
        self.clean_data = self._data_cleaner()

    def _get_raw_data(self):

        # check if location exist
        if os.path.exists(f'{self.location}.htm'):

            modification_timestamp = os.path.getmtime(f'{self.location}.htm')
            modification_date = datetime.date.fromtimestamp(modification_timestamp)

            # check if today's data on disk
            if modification_date == self.scrape_time.date():
                with open('las-palmas-de-gran-canaria.htm', 'r') as f:
                    return f.read()

        url = 'https://www.tidetime.org/europe/spain/las-palmas-de-gran-canaria.htm'
        r = requests.get(url, headers={'user-agent': 'my-app/0.0.1'})
        with open('las-palmas-de-gran-canaria.htm', 'w') as f:
            f.write(r.text)
        with open('las-palmas-de-gran-canaria.htm', 'r') as f:
            return f.read()

    def _data_cleaner(self):
        _tide_table = self._find_tide_table()
        _clean_tide_table = self._clean_tide_table(_tide_table)
        _tides_strings = self._make_tide_strings(_clean_tide_table)
        return _tides_strings

    def _find_tide_table(self):
        position_tide_table_start = self.raw_data.find('<table id="tideTable">')
        position_tide_table_finish = self.raw_data.find('</table>')
        tide_table = self.raw_data[position_tide_table_start:position_tide_table_finish]

        tide_table = tide_table.replace('\n', '')
        tide_table = tide_table.replace('\t', '')

        return tide_table

    @staticmethod
    def _clean_tide_table(tide_table):
        output = []
        is_inside_tag = False
        for i in range(len(tide_table)):
            if tide_table[i] == '>':
                is_inside_tag = True
                continue
            if tide_table[i] == '<':
                is_inside_tag = False
                continue

            if is_inside_tag:
                output.append(tide_table[i])

        clean_tide_table = ''.join(output)
        return clean_tide_table

    @staticmethod
    def _make_tide_strings(clean_tide_table):
        tide_lows = [m.start() for m in re.finditer('Low', clean_tide_table)]
        tide_highs = [m.start() for m in re.finditer('High', clean_tide_table)]
        tides_starts = sorted(tide_lows + tide_highs)

        tides_strings = []
        for i in range(len(tides_starts)):
            try:
                tides_strings.append(clean_tide_table[tides_starts[i]:tides_starts[i + 1]])
            except IndexError:
                tides_strings.append(clean_tide_table[tides_starts[i]:clean_tide_table.rindex(')') + 1])

        return tides_strings


class Tide:
    """
    create Tide class objects from clean scraper data
    """
    def __init__(self, data):
        self.data = data
        self.state = self.get_state()
        self.time_as_string = self.get_time_as_string()
        self.time_as_time_object = self.get_time_as_time_object()
        self.size_as_string = self.get_size_as_string()
        self.size_as_float = self.get_size_as_float()
        self.size_as_integer = self.get_size_as_integer()
        self.datetime_weekly = None

    def __str__(self):
        if self.datetime_weekly:
            return f'{self.state} {self.size_as_string} {self.time_as_string} {self.datetime_weekly}'
        return f'{self.state} {self.size_as_string} {self.time_as_string}'

    def __repr__(self):
        if self.datetime_weekly:
            return f'{self.state} {self.size_as_string} {self.time_as_string} {self.datetime_weekly}'
        return f'{self.state} {self.size_as_string} {self.time_as_string}'

    def get_state(self):
        if 'Low' in self.data:
            return 'Low'
        elif 'High' in self.data:
            return 'High'
        else:
            return ''

    def get_time_as_string(self):
        try:
            time_as_string = re.search('[ 1][0-9]:[0-5][0-9][ap]m', self.data).group()
        except AttributeError:
            return ''

        return self.time_12h_24h_converter(time_as_string)

    @staticmethod
    def time_12h_24h_converter(time_as_string):
        if time_as_string[-2:] == 'am' and time_as_string[:2] == '12':
            return f'00{time_as_string[2:-2]}'

        elif time_as_string[-2:] == 'am':
            return f'{time_as_string[:-2].strip().zfill(5)}'

        elif time_as_string[-2:] == 'pm' and time_as_string[:2] == '12':
            return time_as_string[:-2]

        else:
            return f'{int(time_as_string[:2]) + 12}{time_as_string[2:-2]}'

    def get_time_as_time_object(self):
        # convert string "00:34" to datetime.time(0, 34)
        if self.time_as_string:
            return datetime.time(*[int(x) for x in self.time_as_string.split(':')])
        return None

    def get_size_as_string(self):
        try:
            # size_as_string = re.search('([0-9]\\.[0-9][0-9])', self.data).group()
            size_as_string = re.search('\\([0-9.]+', self.data).group()
            return size_as_string[1:]
        except AttributeError:
            return ''

    def get_size_as_float(self):
        if self.size_as_string:
            return float(self.size_as_string)
        return None

    def get_size_as_integer(self):
        if self.get_time_as_string:
            return int(float(self.size_as_string) * 100)
        return None


class TidesWeekly:
    """
    add weekly timestamps to given list of Tide objects (could be integrated into Tide class)
    """
    def __init__(self, data):
        self.data = data
        self.data_ok = self.verify_data()
        self.tides_weekly_ok = self.build_tides_weekly()

    def verify_data(self):
        return all([isinstance(tide, Tide) for tide in self.data])

    def build_tides_weekly(self):
        if self.data_ok:
            date = datetime.datetime.today().date()
            add_one_day = datetime.timedelta(1)

            _last_tide_time = None
            for tide in self.data:

                if _last_tide_time and _last_tide_time > tide.time_as_time_object:
                    date = date + add_one_day

                dt_weekly = f'{date.day} {date.month} {date.year} ' \
                            f'{tide.time_as_time_object.hour}:' \
                            f'{tide.time_as_time_object.minute}'
                tide.datetime_weekly = datetime.datetime.strptime(dt_weekly, '%d %m %Y %H:%M')

                _last_tide_time = tide.time_as_time_object

        return True


class TidesQueries:
    """
    create all weekly relations between Tide objects
    """
    def __init__(self, tides_weekly):
        self.data = tides_weekly.data
        self.last_tide = self._get_last_tide()
        self.next_tide = self._get_next_tide()
        self.next_low_tide = self._get_next_low_tide()
        self.next_lowest_tide = self._get_next_lowest_tide()
        self.next_high_tide = self._get_next_high_tide()
        self.next_highest_tide = self._get_next_highest_tide()

    def _get_last_tide(self):
        now = datetime.datetime.now()
        for tide in self.data:
            if tide.datetime_weekly - now < datetime.timedelta(0):
                return tide

    def _get_next_tide(self):
        now = datetime.datetime.now()
        for tide in self.data:
            if tide.datetime_weekly - now > datetime.timedelta(0):
                return tide

    def _get_next_low_tide(self):
        now = datetime.datetime.now()
        for tide in self.data:
            if tide.datetime_weekly - now > datetime.timedelta(0) and tide.state == 'Low':
                return tide

    def _get_next_high_tide(self):
        now = datetime.datetime.now()
        for tide in self.data:
            if tide.datetime_weekly - now > datetime.timedelta(0) and tide.state == 'High':
                return tide

    def _get_next_lowest_tide(self):
        now = datetime.datetime.now()
        _tmp = []
        for tide in self.data:
            if tide.datetime_weekly - now > datetime.timedelta(0) and tide.state == 'Low':
                _tmp.append(tide)
        return sorted(_tmp, key=lambda x: x.size_as_float)[0]

    def _get_next_highest_tide(self):
        now = datetime.datetime.now()
        _tmp = []
        for tide in self.data:
            if tide.datetime_weekly - now > datetime.timedelta(0) and tide.state == 'High':
                _tmp.append(tide)
        return sorted(_tmp, key=lambda x: x.size_as_float)[-1]


class TidesModel:
    """
    Model layer - access via tidies_queries attribute
    """
    def __init__(self):
        self._tides_strings = Scraper().clean_data
        self._tides_weekly = TidesWeekly([Tide(tide) for tide in self._tides_strings])
        self.tides_queries = TidesQueries(self._tides_weekly)
