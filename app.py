import re
from datetime import datetime

reports = [
    "EHAM 020825Z 21022KT 190V250 9999 FEW008 SCT018 BKN022 17/15 Q1002 NOSIG",
    "TNCB 020755Z AUTO 11004KT 9999 NCD 26/25 Q1008",
    "KLAX 020753Z 05004KT 0SM R25L/1800V3000FT FG VV002 17/16 A3006 RMK AO2 SLP177 T01670161 402440128 $",
    "EGPK 020920Z 25010G21KT 8000 -RA FEW014 SCT020 BKN042 09/08 Q0991"
]

def find(regex, string):
    matches = re.search(regex, string)

    if not matches:
        return None

    return matches.group().strip()

for report in reports:
    print(report)

    obj = {
        'ident': find(r'^\S{4}\s', report),
        'raw': report
    }

    # Get date and time
    reported = find(r'\s\d{6}Z\s', report).replace('Z', '')
    dt = datetime.strptime(reported, '%d%H%M')
    dt = dt.replace(year=datetime.today().year, month=datetime.today().month)
    obj['reported'] = dt.isoformat()

    # Get wind info
    wind = re.search(r'\s(\d{3}|VRB)(\d{2})(?:G(\d*))?KT\s(?:(\d{3})V(\d{3})\s)?', report)  # https://regex101.com/r/wuyEsI/1
    if wind:
        wind_obj = {
            'direction': int(wind.group(1)),
            'speed': int(wind.group(2))
        }

        if wind.group(3):
            wind_obj['gust'] = int(wind.group(3))

        if wind.group(4) and wind.group(5):
            wind_obj['variable'] = {
                'from': int(wind.group(4)),
                'to': int(wind.group(5))
            }

        obj['wind'] = wind_obj

    # Get temperatures
    temps = re.search(r'\s(\d{2})/(\d{2})\s', report)
    if temps:
        obj['temperatures'] = {
            'temperature': int(temps.group(1)),
            'dew_point': int(temps.group(2)),
        }

    import json
    print(json.dumps(obj, indent=4, sort_keys=True))
