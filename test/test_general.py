import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metar_parser import Metar

REPORTS = [
    'EHAM 020825Z 21022KT 190V250 9999 FEW008 SCT018 BKN022 17/15 Q1002 NOSIG',
    'K2W6 021035Z AUTO 02/M05 A3004 RMK AO1',
    'KIAB 020956Z COR AUTO 17005KT 10SM CLR 04/M05 A3045 RMK AO2 SLP318 T00391053 COR 1000',
    'PHOG 020954Z COR 00000KT 10SM SCT022 24/19 A3006 RMK AO2 SLP182 T02440189 403170206',
]

class TestGeneral(unittest.TestCase):
    def test_ident(self):
        for i, ident in enumerate(['EHAM', 'K2W6', 'KIAB', 'PHOG']):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_ident(), ident)

    def test_report_modifier(self):
        for i, ident in enumerate([None, 'AUTO', 'COR', 'COR']):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_report_modifier(), ident)

if __name__ == '__main__':
    unittest.main()
