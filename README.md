# python-metar-extractor
Extracts values from METAR reports.

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
| visibility | | object | contains visibility data
| visibility/distance | specified by `visibility/distance_unit` | int | visibility distance
| visibility/distance_unit |  | int | unit of visibility distance
| wind | | object | contains wind data
| wind/direction | degrees or `'VRB'` | int or string | wind direction
| wind/gust | knots | int | gust speed
| wind/speed | specified by `wind/speed_unit` | int | wind speed
| wind/speed_unit |  | int | unit of wind speed
| wind/variable_direction | degrees | list | contains variable wind directions
