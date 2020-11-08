import re
from datetime import datetime
import json
from fractions import Fraction

class Report:
    def find(self, regex, string):
        matches = re.search(regex, string)
        if not matches:
            return None
        return matches.group().strip()

    # Try converting to int, if fails, return string
    def int_or_str(self, string):
        try:
            return int(string)
        except ValueError:
            return string.strip()

    def __init__(self, report):
        report = report.strip()

        self.data = {
            'raw': report,
            'decoded': False
        }

        # Split report into main parts: ident, date+time, body, remarks
        parts = re.match(r'^(\S{4})\s*(.*?Z)(.*?)(?:RMK(.*))?$', report)    # https://regex101.com/r/Nq5xhk/1

        if not parts:
            return

        self.data['ident'] = parts.group(1)

        # Get date and time
        if parts.group(2):
            try:
                dt = datetime.strptime(parts.group(2), '%d%H%M%z')
                dt = dt.replace(year=datetime.today().year, month=datetime.today().month)
                self.data['reported'] = dt.isoformat()
            except ValueError as e:
                return

        if parts.group(3):
            # Get wind data
            wind = re.search(r'\s(?:([\d\/]{3}|VRB)([\d\/]{2,3}))(?:G(\d{2,3}))?(KT|MPS)(?:\s(\d{3})V(\d{3})\s)?', parts.group(3))  # https://regex101.com/r/wuyEsI/3
            if wind:
                obj = dict()

                # Add main wind data
                for index, key in enumerate(['direction', 'speed', 'gust']):
                    value = wind.group(index+1)

                    if value and not '/' in value:
                        obj[key] = self.int_or_str(value)

                if 'speed' in obj:
                    obj['speed_unit'] = wind.group(4).lower()

                # Add variable wind direction
                if wind.group(5) and wind.group(6) and not ('/' in wind.group(5) or '/' in wind.group(6)):
                    obj['variable_direction'] = [self.int_or_str(wind.group(5)), self.int_or_str(wind.group(6))]

                if len(obj) > 0:
                    self.data['wind'] = obj

            # Get temperature data
            temps = re.search(r'\s(M?\d{2})/(M?\d{2})', parts.group(3))    # https://regex101.com/r/oqplsG/1
            if temps:
                obj = dict()

                for index, key in enumerate(['temperature', 'dew_point']):
                    value = temps.group(index+1).replace('M', '-')
                    if value and not '/' in value:
                        obj[key] = self.int_or_str(value)

                if len(obj) > 0:
                    self.data['temperatures'] = obj

            # Get report modifier
            for modifier in ['AUTO', 'COR']:    
                # Note: In case both AUTO and COR are present, COR will be used as per https://www.ofcm.gov/publications/fmh/FMH1/FMH1.pdf
                # (p. 58: "In the event of a corrected METAR or SPECI, the report modifier, COR, shall be substituted in place of AUTO")
                if modifier in parts.group(3):
                    self.data['report_modifier'] = modifier

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
                elif visibility.group(3):   # '2 1/4SM', 'M1/4SM'
                    # Convert fraction to float (https://stackoverflow.com/a/1806309)
                    # Note: negative values fail using this method. Since only positive values are handled this should not be an issue.
                    distance = float(sum(Fraction(s) for s in visibility.group(3).split()))

                    # The character 'M' is used to define a visibility distance less than the value.
                    # We'll use negative values to indicate this.
                    if visibility.group(2):
                        distance = distance * -1

                    if visibility.group(4):
                        unit = visibility.group(4)

                obj = dict()

                if distance:
                    obj['distance'] = distance

                    if unit:
                        obj['distance_unit'] = unit

                if len(obj) > 0:
                    self.data['visibility'] = obj

        self.data['decoded'] = True

    def json(self):
        return json.dumps(self.data, indent=4, sort_keys=True)

    def decoded(self):
        return self.data['decoded']
