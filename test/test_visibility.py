import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metar_parser import Metar

REPORTS = [
    'ZMUB 021000Z VRB01MPS CAVOK M09/M13 Q1025 NOSIG RMK QFE660.4 66',

    "EHAM 020825Z 21022KT 190V250 9999 FEW008 SCT018 BKN022 17/15 Q1002 NOSIG",
    "EGPK 020920Z 25010G21KT 8000 -RA FEW014 SCT020 BKN042 09/08 Q0991",
    'MTPP 020959Z AUTO /////KT 9000 ////// ///// Q//// A//// NOSIG',

    "PAUN 131256Z AUTO 08006KT 10SM SCT021 M04/M05 A2931 RMK AO2 SNE15 SLP927 P0000 T10391050 FZRANO",
    'CYHK 020945Z AUTO 31015KT 4SM -SN BKN034 M16/M18 A2998 RMK SLP162',
    'KLAX 020753Z 05004KT 0SM R25L/1800V3000FT FG VV002 17/16 A3006 RMK AO2 SLP177 T01670161 402440128',
    'KWBF 020945Z AUTO 02016G24KT M8SM OVC037 22/15 A3025 RMK A01',
    'KSXS 021031Z AUTO M 10SM CLR 08/00 A3032 RMK AO2 SLP269',

    'KELZ 020956Z AUTO 31017G23KT 1/2SM SN FZFG BKN007 OVC011 M03/M04 A2986 RMK AO2 PK WND 32035/0901 SLP135 P0001 T10331039',
    'CYBC 021001Z AUTO 33003KT 2 1/4SM R10/5500FT/N -RA BR BKN024 OVC045 04/03 A2926 RMK VIS VRB 5/8-3 SLP912',
    'CYFC 021002Z AUTO 33002KT M3/4SM R09/5000FT/U -RA BR OVC029 10/10 A2917 RMK PRESFR SLP880 DENSITY ALT 200FT',
]

class TestVisibility(unittest.TestCase):
    def test_distance(self):
        for i, value in enumerate([10000, 9999, 8000, 9000, 10, 4, 0, -8, -10, 0.5, 2.25, -0.75]):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_visibility_distance(), value)

    def test_unit(self):
        for i, value in enumerate(['m', 'm', 'm', 'm', 'sm', 'sm', 'sm', 'sm', 'sm', 'sm', 'sm', 'sm']):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_visibility_distance_unit(), value)
 
    def test_converted_distance(self):
        for i, value in enumerate([10000, 9999, 8000, 9000, 18520, 7408, 0, 14816, 18520, 926, 4167, 1389]):
            report = Metar.Report(REPORTS[i])
            self.assertEqual(report.get_visibility_distance_m(), value)

if __name__ == '__main__':
    unittest.main()
