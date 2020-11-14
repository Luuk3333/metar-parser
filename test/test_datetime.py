import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metar_parser import Metar
from datetime import datetime

REPORTS = [
    "EHAM 020825Z 21022KT 190V250 9999 FEW008 SCT018 BKN022 17/15 Q1002 NOSIG",
    'CYHK 020945Z AUTO 31015KT 4SM -SN BKN034 M16/M18 A2998 RMK SLP162',
    "PAUN 131256Z AUTO 08006KT 10SM SCT021 M04/M05 A2931 RMK AO2 SNE15 SLP927 P0000 T10391050 FZRANO",
]

DT = datetime.today()
YEAR_MONTH = DT.strftime('%Y-%m-')

class TestVisibility(unittest.TestCase):
    def test_iso(self):
        for i, value in enumerate([
                YEAR_MONTH + '02T08:25:00+00:00',
                YEAR_MONTH + '02T09:45:00+00:00',
                YEAR_MONTH + '13T12:56:00+00:00',
            ]):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_reported(), value)

    def test_date(self):
        for i, value in enumerate([
                YEAR_MONTH + '02',
                YEAR_MONTH + '02',
                YEAR_MONTH + '13',
            ]):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_date(), value)

    def test_time(self):
        for i, value in enumerate(['08:25', '09:45', '12:56']):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_time(), value)

if __name__ == '__main__':
    unittest.main()
