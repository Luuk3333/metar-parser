import re
from datetime import datetime

reports = [
    "EHAM 020825Z 21022KT 190V250 9999 FEW008 SCT018 BKN022 17/15 Q1002 NOSIG",
    "TNCB 020755Z AUTO 11004KT 9999 NCD 26/25 Q1008",
    "KLAX 020753Z 05004KT 0SM R25L/1800V3000FT FG VV002 17/16 A3006 RMK AO2 SLP177 T01670161 402440128 $"
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
    reported = find(r'\s\S{6}Z\s', report).replace('Z', '')
    dt = datetime.strptime(reported, '%d%H%M')
    dt = dt.replace(year=datetime.today().year, month=datetime.today().month)
    obj['reported'] = dt.isoformat()

    import json
    print(json.dumps(obj, indent=4))
