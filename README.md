# python-metar-decoder
A METAR decoder written in Python.

## Output format
| **key** | **unit** | **datatype** | **description**
|-|-|-|-|
| decoded | | boolean | decoding status
| indent | | string | weather station identifier
| raw | | string | input METAR
| report_modifier | AUTO=a fully automated report with no human intervention or oversight, COR=a corrected report | string |
| reported | ISO 8601 | string | date and time of report
| temperatures | | object | contains temperature data
| temperatures/dew_point | degrees Celsius | int | dew point temperature
| temperatures/temperature | degrees Celsius | int | temperature
| wind | | object | contains wind data
| wind/direction | degrees or `'VRB'` | int or string | wind direction
| wind/gust | knots | int | gust speed
| wind/speed | specified by `wind/speed_unit` | int | wind speed
| wind/speed_unit |  | int | unit of wind speed
| wind/variable_direction | degrees | list | contains variable wind directions