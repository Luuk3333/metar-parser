import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metar_parser import Metar

REPORTS_WIND = [
    "EHAM 020825Z 21022KT 190V250 9999 FEW008 SCT018 BKN022 17/15 Q1002 NOSIG",
    "EGPK 020920Z 25010G21KT 8000 -RA FEW014 SCT020 BKN042 09/08 Q0991",
    'UTDL 021030Z 08004MPS 7000 NSC 18/M04 Q1022 R26/CLRD70 NOSIG RMK QFE729/0972',
    'ZMUB 021000Z VRB09G18MPS CAVOK M09/M13 Q1025 NOSIG RMK QFE660.4 66',
]

REPORTS_VISIBILITY = [
    'ZMUB 021000Z VRB01MPS CAVOK M09/M13 Q1025 NOSIG RMK QFE660.4 66',
    "EHAM 020825Z 21022KT 190V250 9999 FEW008 SCT018 BKN022 17/15 Q1002 NOSIG",
    "PAUN 131256Z AUTO 08006KT 10SM SCT021 M04/M05 A2931 RMK AO2 SNE15 SLP927 P0000 T10391050 FZRANO",
    'KWBF 020945Z AUTO 02016G24KT M8SM OVC037 22/15 A3025 RMK A01',
    'KELZ 020956Z AUTO 31017G23KT 1/2SM SN FZFG BKN007 OVC011 M03/M04 A2986 RMK AO2 PK WND 32035/0901 SLP135 P0001 T10331039',
    'CYBC 021001Z AUTO 33003KT 2 1/4SM R10/5500FT/N -RA BR BKN024 OVC045 04/03 A2926 RMK VIS VRB 5/8-3 SLP912',
    'CYFC 021002Z AUTO 33002KT M3/4SM R09/5000FT/U -RA BR OVC029 10/10 A2917 RMK PRESFR SLP880 DENSITY ALT 200FT',
]

class TestConversions(unittest.TestCase):
    def test_wind_speed(self):
        for i, value in enumerate([11.32, 5.14, 4, 9]):
            report = Metar.Report(REPORTS_WIND[i])

            # Make sure returned value is a number that can be rounded
            if report.get_wind_speed_ms():
                self.assertEqual(round(report.get_wind_speed_ms(), 2), value)
            else:
                self.assertEqual(report.get_wind_speed_ms(), value)

    def test_wind_gust(self):
        for i, value in enumerate([None, 10.80, None, 18]):
            report = Metar.Report(REPORTS_WIND[i])

            if report.get_wind_gust_ms():
                self.assertEqual(round(report.get_wind_gust_ms(), 2), value)
            else:
                self.assertEqual(report.get_wind_gust_ms(), value)

    def test_visibility_distance(self):
        for i, value in enumerate([10000, 9999, 18520, -14816, 926, 4167, -1389]):
            report = Metar.Report(REPORTS_VISIBILITY[i])
            self.assertEqual(report.get_visibility_distance_m(), value)

if __name__ == '__main__':
    unittest.main()
