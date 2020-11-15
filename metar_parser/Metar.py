import re
from datetime import datetime
import json
from fractions import Fraction

SPEED_TO_MS = {
    'mps': 1,
    'kt': 0.514444
}

DISTANCE_TO_M = {
    'm': 1,
    'sm': 1852
}

class Report:
    """A parsed METAR report."""
    def _convert_to_ms(self, value, unit):
        """Convert a value to meters per second

        Parameters
        ----------
        value : int/float
          Input value.
        unit : str
          Unit to convert from.
        """
        if value and unit and unit in SPEED_TO_MS:
            return value * SPEED_TO_MS[unit]
        return None

    def _convert_to_m(self, value, unit):
        """Convert a value to meters

        Parameters
        ----------
        value : int/float
          Input value.
        unit : str
          Unit to convert from.
        """
        if value and unit and unit in DISTANCE_TO_M:
            return value * DISTANCE_TO_M[unit]
        return None

    def __int_or_str(self, string):
        """Try converting to int, if fails, return string."""
        if not string:
            return None

        string = string.strip()

        if '/' in string:
            return None

        try:
            return int(string)
        except ValueError:
            return string

    def __init__(self, raw):
        """Parse an input METAR report.

        Parameters
        ----------
        raw : str
          Input METAR report.
        """
        self.raw = raw.strip()  # Input METAR report
        self.parsed = False
        self.ident = None
        self.report_modifier = None

        self.reported = None
        self.date = None
        self.time = None

        self.wind_direction = None
        self.wind_speed = None
        self.wind_speed_unit = None
        self.wind_gust = None
        self.wind_variable_directions = None
        self.wind_speed_ms = None
        self.wind_gust_ms = None

        self.temperature = None
        self.dew_point = None

        self.visibility_distance = None
        self.visibility_distance_unit = None
        self.visibility_distance_m = None

        # Split report into main parts: ident, date+time, body, remarks
        parts = re.match(r'^(\S{4})\s*(.*?Z)(.*?)(?:RMK(.*))?$', self.raw)  # https://regex101.com/r/Nq5xhk/1

        if not parts:
            return

        self.ident = parts.group(1)

        # Get date and time
        if parts.group(2):
            try:
                dt = datetime.strptime(parts.group(2), '%d%H%M%z')
                dt = dt.replace(year=datetime.today().year, month=datetime.today().month)
                self.reported = dt.isoformat()
                self.date = dt.strftime('%Y-%m-%d')
                self.time = dt.strftime('%H:%M')
            except ValueError as e:
                return

        if parts.group(3):
            # Get wind data
            wind = re.search(r'\s(?:([\d\/]{3}|VRB)([\d\/]{2,3}))(?:G(\d{2,3}))?(KT|MPS)(?:\s(\d{3})V(\d{3})\s)?', parts.group(3))  # https://regex101.com/r/wuyEsI/3
            if wind:
                # Add main wind data
                self.wind_direction = self.__int_or_str(wind.group(1))
                self.wind_speed = self.__int_or_str(wind.group(2))
                self.wind_gust = self.__int_or_str(wind.group(3))

                if self.wind_speed:
                    self.wind_speed_unit = wind.group(4).lower()

                # Add variable wind direction
                variable_directions = [
                    self.__int_or_str(wind.group(5)),
                    self.__int_or_str(wind.group(6))
                ]

                if variable_directions[0] and variable_directions[1]:
                    self.wind_variable_directions = variable_directions

                if self.wind_speed_unit:
                    if self.wind_speed:
                        self.wind_speed_ms = self._convert_to_ms(self.wind_speed, self.wind_speed_unit)

                    if self.wind_gust:
                        self.wind_gust_ms = self._convert_to_ms(self.wind_gust, self.wind_speed_unit)

            # Get temperature data
            temps = re.search(r'\s(M?\d{2})/(M?\d{2})', parts.group(3))    # https://regex101.com/r/oqplsG/1
            if temps:
                temperature = temps.group(1).replace('M', '-')
                self.temperature = self.__int_or_str(temperature)

                dew_point = temps.group(2).replace('M', '-')
                self.dew_point = self.__int_or_str(dew_point)

            # Get report modifier
            for modifier in ['AUTO', 'COR']:    
                # Note: In case both AUTO and COR are present, COR will be used as per https://www.ofcm.gov/publications/fmh/FMH1/FMH1.pdf
                # (p. 58: "In the event of a corrected METAR or SPECI, the report modifier, COR, shall be substituted in place of AUTO")
                if modifier in parts.group(3):
                    self.report_modifier = modifier

            # Get visibility data
            visibility = re.search(r'\s(?:(\d{4})\s|(M)?([\d\s/]{1,5})(SM)|(CAVOK))', parts.group(3))   # https://regex101.com/r/YWZkDI/2/
            if visibility:
                distance = None
                unit = None

                # Check for several visibilty formats
                if visibility.group(5): # 'CAVOK'
                    distance = 10000
                    unit = 'm'
                elif visibility.group(1):   # '8000', '9999'
                    distance = int(visibility.group(1))
                    unit = 'm'
                elif visibility.group(3):   # '10SM', 2 1/4SM', 'M1/4SM'
                    if '/' in visibility.group(3):
                        # Convert fraction to float (https://stackoverflow.com/a/1806309)
                        # Note: negative values fail using this method. Since only positive values are handled this should not be an issue.
                        distance = float(sum(Fraction(s) for s in visibility.group(3).split()))
                    else:
                        distance = self.__int_or_str(visibility.group(3))

                    # The character 'M' is used to define a visibility distance less than the value.
                    # We'll use negative values to indicate this.
                    if visibility.group(2):
                        distance = distance * -1

                    if visibility.group(4):
                        unit = visibility.group(4).lower()

                if distance and unit:
                    self.visibility_distance_m = self._convert_to_m(distance, unit)

                self.visibility_distance = distance
                self.visibility_distance_unit = unit

        self.parsed = True


    def wind(self):
        """Return the parsed wind data."""
        return {
            'direction': self.wind_direction,
            'speed': self.wind_speed,
            'speed_unit': self.wind_speed_unit,
            'gust': self.wind_gust,
            'variable_directions': self.wind_variable_directions,
            'speed_ms': self.wind_speed_ms,
            'gust_ms': self.wind_gust_ms
        }

    def temperatures(self):
        """Return the parsed temperature data."""
        return {
            'temperature': self.temperature,
            'dew_point': self.dew_point
        }

    def visibility(self):
        """Return the parsed visibility data."""
        return {
            'distance': self.visibility_distance,
            'distance_unit': self.visibility_distance_unit,
            'distance_m': self.visibility_distance_m
        }

    def result(self):
        """Return the parsed report."""
        return {
            'raw': self.raw,
            'parsed': self.parsed,
            'ident': self.ident,
            'reported': self.reported,
            'date': self.date,
            'time': self.time,
            'report_modifier': self.report_modifier,
            'wind': self.wind(),
            'temperatures': self.temperatures(),
            'visibility': self.visibility()
        }

    def json(self, pretty=False):
        """Return the parsed report as JSON.        

        Parameters
        ----------
        pretty : boolean
          Beautify JSON output.
        """
        if pretty:
            return json.dumps(self.result(), indent=4, sort_keys=True)
        
        return json.dumps(self.result())

    def get_raw(self):
        """Return the raw METAR input."""
        return self.raw

    def is_parsed(self):
        """Indicate if the report could be parsed."""
        return self.parsed

    def get_ident(self):
        """Return the weather station identifier."""
        return self.ident

    def get_report_modifier(self):
        """Return the report modifier"""
        return self.report_modifier


    def get_reported(self):
        """Return the reported date and time"""
        return self.reported

    def get_date(self):
        """Return the date of the report"""
        return self.date

    def get_time(self):
        """Return the time of the report"""
        return self.time


    def get_wind_direction(self):
        """Return the wind direction"""
        return self.wind_direction

    def get_wind_speed(self):
        """Return the wind speed"""
        return self.wind_speed

    def get_wind_speed_unit(self):
        """Return the wind speed unit"""
        return self.wind_speed_unit

    def get_wind_gust(self):
        """Return the wind gust speed"""
        return self.wind_gust

    def get_wind_variable_directions(self):
        """Return the variable wind directions"""
        return self.wind_variable_directions

    def get_wind_speed_ms(self):
        """Return the wind speed in m/s"""
        return self.wind_speed_ms

    def get_wind_gust_ms(self):
        """Return the wind gust speed in m/s"""
        return self.wind_gust_ms


    def get_temperature(self):
        """Return the temperature"""
        return self.temperature

    def get_dew_point(self):
        """Return the dew point"""
        return self.dew_point


    def get_visibility_distance(self):
        """Return the visibility distance"""
        return self.visibility_distance

    def get_visibility_distance_unit(self):
        """Return the visibility distance unit"""
        return self.visibility_distance_unit

    def get_visibility_distance_m(self):
        """Return the wind speed in m"""
        return self.visibility_distance_m
