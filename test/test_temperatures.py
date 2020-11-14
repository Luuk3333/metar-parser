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
    'ZMUB 021000Z VRB01MPS CAVOK M09/M13 Q1025 NOSIG RMK QFE660.4 66',
    'CYHK 020945Z AUTO 31015KT 4SM -SN BKN034 M16/M18 A2998 RMK SLP162',
]

class TestTemperatures(unittest.TestCase):
    def test_temperature(self):
        for i, value in enumerate([17, 2, 18, -4, -9, -16]):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_temperature(), value)

    def test_dew_point(self):
        for i, value in enumerate([15, -5, -4, -5, -13, -18]):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_dew_point(), value)

if __name__ == '__main__':
    unittest.main()
