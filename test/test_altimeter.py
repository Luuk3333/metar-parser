import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metar_parser import Metar

REPORTS = [
    'EHAM 020825Z 21022KT 190V250 9999 FEW008 SCT018 BKN022 17/15 Q1002 NOSIG',
    'K2W6 021035Z AUTO 02/M05 A3004 RMK AO1',
    'UTDL 021030Z 08004MPS 7000 NSC 18/M04 Q1022 R26/CLRD70 NOSIG RMK QFE729/0972',
    'PAUN 131256Z AUTO 08006KT 10SM SCT021 M04/M05 A2931 RMK AO2 SNE15 SLP927 P0000 T10391050 FZRANO',
]

class TestAltimeter(unittest.TestCase):
    def test_value(self):
        for i, value in enumerate([1002, 30.04, 1022, 29.31]):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_altimeter_pressure(), value)

    def test_unit(self):
        for i, value in enumerate(['hPa', 'inHg', 'hPa', 'inHg']):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_altimeter_pressure_unit(), value)

    def test_converted(self):
        for i, value in enumerate([100200, 101440.57, 102200, 98975.47]):
            report = Metar.Report(REPORTS[i])

            if report.get_altimeter_pressure_pa():
                self.assertEqual(round(report.get_altimeter_pressure_pa(), 2), value)
            else:
                self.assertEqual(report.get_altimeter_pressure_pa(), value)

if __name__ == '__main__':
    unittest.main()
