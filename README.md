# metar-parser
Parses METAR reports and extracts values.

- [Usage](#usage)
- [Output format](#output-format)
- [Development](#development)
    - [Download repo](#download-repo)
    - [Run tests](#run-tests)

## Usage
```
from metar_parser import Metar

report = Metar.Report('EHAM 020825Z 21022KT 190V250 9999 FEW008 SCT018 BKN022 17/15 Q1002 NOSIG')
if report.is_parsed():
    print('Station: {} @ {}'.format(report.get_ident(), report.get_time()))
    print('Wind speed: {} {}'.format(report.get_wind_speed(), report.get_wind_speed_unit()))
```
which outputs:
```
Station: EHAM @ 08:25
Wind speed: 22 kt
```
See [sample.py](sample.py) for more examples.

## Output format
Notes:
- The getter `json()` will return the parsed report in JSON.
- The current year and month will be used when returning the date.
- Converted values are useful for sorting.

| **JSON key** | **getter** | **unit** | **datatype** | **description** |
|-|-|-|-|-|
| altimeter | `altimeter()` |  | object | contains altimeter data |
| altimeter/pressure | `get_altimeter_pressure` | specified by `altimeter/pressure_unit` | int or float | pressure at station
| altimeter/pressure_pa | `get_altimeter_pressure_pa` | pascals | float | converted pressure
| altimeter/pressure_unit | `get_altimeter_pressure_unit` | | string | unit of pressure
| date | `get_date()` | `'YYYY-MM-DD'` | string | date of report |
| ident | `get_ident()` |  | string | weather station identifier |
| parsed | `is_parsed()` |  | boolean | parsed status |
| raw | `get_raw()` |  | string | input METAR report |
| report_modifier | `get_report_modifier()` | `'AUTO'` (fully automated report), `'COR'` (corrected report) | string | auto/corrected modifier |
| reported | `get_reported()` | ISO 8601 (`'YYYY-MM-DDTHH:MM:SS+HH:MM'`) | string | date and time of report |
| temperatures | `temperatures()` |  | object | contains temperature data |
| temperatures/dew_point | `get_dew_point()` | degrees Celsius | int | dew point |
| temperatures/temperature | `get_temperature()` | degrees Celsius | int | temperature |
| time | `get_time()` | `'HH:MM'` | string | time of report |
| visibility | `visibility()` |  | object | contains visibility data |
| visibility/distance | `get_visibility_distance()` | specified by `visibility/distance_unit` | int or float | visibility distance (negative value to be interpreted as 'visibility less than value') |
| visibility/distance_m | `get_visibility_distance_m()` | meters | int or float | converted visibility distance |
| visibility/distance_str | `get_visibility_distance_str()` | | string | visibility including 'less than' symbol and unit if applicable, retaining fractions |
| visibility/distance_unit | `get_visibility_distance_unit()` |  | string | unit of visibility distance |
| wind | `wind()` |  | object | contains wind data |
| wind/direction | `get_wind_direction()` | degrees or `'VRB'` | int or string | wind direction |
| wind/gust | `get_wind_gust()` | specified by `wind/speed_unit` | int | gust speed |
| wind/gust_ms | `get_wind_gust_ms()` | meters per second | int or float | converted gust speed |
| wind/speed | `get_wind_speed()` | specified by `wind/speed_unit` | int | wind speed |
| wind/speed_ms | `get_wind_speed_ms()` | meters per second | int or float | converted wind speed |
| wind/speed_unit | `get_wind_speed_unit()` |  | string | unit of wind speed |
| wind/variable_directions | `get_wind_variable_directions()` | degrees | list | contains variable wind directions |

## Development
### Download repo
```
git clone https://github.com/Luuk3333/metar-parser
cd metar-parser
```
### Run tests
```
python3 -m unittest
```
