import re
from datetime import datetime
import json

reports = [
    "EHAM 020825Z 21022KT 190V250 9999 FEW008 SCT018 BKN022 17/15 Q1002 NOSIG",
    "TNCB 020755Z AUTO 11004KT 9999 NCD 26/25 Q1008",
    "KLAX 020753Z 05004KT 0SM R25L/1800V3000FT FG VV002 17/16 A3006 RMK AO2 SLP177 T01670161 402440128 $",
    "EGPK 020920Z 25010G21KT 8000 -RA FEW014 SCT020 BKN042 09/08 Q0991"
]

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

        self.data['decoded'] = True

    def json(self):
        return json.dumps(self.data, indent=4, sort_keys=True)

    def decoded(self):
        return self.data['decoded']

for raw in reports:
    report = Report(raw)
    print(report.json())
