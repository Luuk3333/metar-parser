# metar-parser
Parses METAR reports and extracts values.

## JSON Output Format
Notes:
- A negative visibility distance means the visibility is less than the distance. This does not apply to converted values.

| **key** | **unit** | **datatype** | **description**
|-|-|-|-|
| date | | string | date of report (YYYY-MM-DD)
| ident | | string | weather station identifier
| parsed | | boolean | parsed status
| raw | | string | input METAR
| report_modifier | AUTO=a fully automated report with no human intervention or oversight, COR=a corrected report | string |
| reported | ISO 8601 | string | date and time of report
| temperatures | | object | contains temperature data
| temperatures/dew_point | degrees Celsius | int | dew point temperature
| temperatures/temperature | degrees Celsius | int | temperature
| time | | string | time of report (HH:MM)
| visibility | | object | contains visibility data
| visibility/distance | specified by `visibility/distance_unit` | int | visibility distance
| visibility/distance_m | meters | int or float | converted visibility distance in meters
| visibility/distance_unit |  | int | unit of visibility distance
| wind | | object | contains wind data
| wind/direction | degrees or `'VRB'` | int or string | wind direction
| wind/gust | specified by `wind/speed_unit` | int | gust speed
| wind/gust_ms | meters per second | int or float | converted gust speed in meters per second
| wind/speed | specified by `wind/speed_unit` | int | wind speed
| wind/speed_ms | meters per second | int or float | converted wind speed in meters per second
| wind/speed_unit |  | int | unit of wind speed
| wind/variable_directions | degrees | list | contains variable wind directions
