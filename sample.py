from metar_parser import Metar

reports = [
    "EHAM 020825Z 21022KT 190V250 9999 FEW008 SCT018 BKN022 17/15 Q1002 NOSIG",
    "EGPK 020920Z 25010G21KT 8000 -RA FEW014 SCT020 BKN042 09/08 Q0991",
    "PAUN 131256Z AUTO 08006KT 10SM SCT021 M04/M05 A2931 RMK AO2 SNE15 SLP927 P0000 T10391050 FZRANO",
]

report = Metar.Report(reports[0])
if report.is_parsed:
    print(report.json(pretty=True))

print('--------')

report = Metar.Report(reports[1])
if report.is_parsed:
    visibility = report.visibility()
    print(report.get_raw())
    print('Visibility: {} {}'.format(visibility['distance'], visibility['distance_unit']))

print('--------')

report = Metar.Report(reports[2])
if report.is_parsed:
    temps = report.temperatures()
    print(report.get_raw())
    print('Temperature: {}°C'.format(temps['temperature']))
    print('Dew point: {}°C'.format(temps['dew_point']))
