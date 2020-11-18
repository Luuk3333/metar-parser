import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metar_parser import Metar

REPORTS = [
    "EHAM 020825Z 21022KT 190V250 9999 FEW008 SCT018 BKN022 17/15 Q1002 NOSIG",
    "EGPK 020920Z 25010G21KT 8000 -RA FEW014 SCT020 BKN042 09/08 Q0991",
    "PAUN 131256Z AUTO 08006KT 10SM SCT021 M04/M05 A2931 RMK AO2 SNE15 SLP927 P0000 T10391050 FZRANO",
    'UTDL 021030Z 08004MPS 7000 NSC 18/M04 Q1022 R26/CLRD70 NOSIG RMK QFE729/0972',
    'ZMUB 021000Z VRB01MPS CAVOK M09/M13 Q1025 NOSIG RMK QFE660.4 66',
    'ZMUB 021000Z VRB09G18MPS CAVOK M09/M13 Q1025 NOSIG RMK QFE660.4 66',
]

class TestWind(unittest.TestCase):
    def test_direction(self):
        for i, value in enumerate([210, 250, 80, 80, 'VRB', 'VRB']):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_wind_direction(), value)

    def test_speed(self):
        for i, value in enumerate([22, 10, 6, 4, 1, 9]):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_wind_speed(), value)

    def test_speed_unit(self):
        for i, value in enumerate(['kt', 'kt', 'kt', 'mps', 'mps', 'mps']):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_wind_speed_unit(), value)

    def test_wind_gust(self):
        for i, value in enumerate([None, 21, None, None, None, 18]):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_wind_gust(), value)

    def test_wind_variable_directions(self):
        for i, value in enumerate([[190, 250], None, None, None, None, None]):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_wind_variable_directions(), value)

    def test_converted_wind_speed(self):
        for i, value in enumerate([11.32, 5.14, 3.09, 4, 1, 9]):
            report = Metar.Report(REPORTS[i])

            # Make sure returned value is a number that can be rounded
            if report.get_wind_speed_ms():
                self.assertEqual(round(report.get_wind_speed_ms(), 2), value)
            else:
                self.assertEqual(report.get_wind_speed_ms(), value)

    def test_converted_wind_gust(self):
        for i, value in enumerate([None, 10.8, None, None, None, 18]):
            report = Metar.Report(REPORTS[i])

            if report.get_wind_gust_ms():
                self.assertEqual(round(report.get_wind_gust_ms(), 2), value)
            else:
                self.assertEqual(report.get_wind_gust_ms(), value)

if __name__ == '__main__':
    unittest.main()
