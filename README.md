# metar-parser
Parses METAR reports and extracts values.

## Output format
Notes:
- A negative visibility distance means the visibility is less than the distance. This does not apply to converted values.
- The getter `json()` will return the parsed report in JSON.
- The current year and month will be used when returning the date.

| **JSON key** | **getter** | **unit** | **datatype** | **description** |
|-|-|-|-|-|
| date | `get_date()` | `'YYYY-MM-DD'` | string | date of report |
| ident | `get_ident()` |  | string | weather station identifier |
| parsed | `is_parsed()` |  | boolean | parsed status |
| raw | `get_raw()` |  | string | input METAR |
| report_modifier | `get_report_modifier()` | AUTO=a fully automated report with no human intervention or oversight, COR=a corrected report | string |  |
| reported | `get_reported()` | ISO 8601 | string | date and time of report |
| temperatures | `temperatures()` |  | object | contains temperature data |
| temperatures/dew_point | `get_dew_point()` | degrees Celsius | int | dew point temperature |
| temperatures/temperature | `get_temperature()` | degrees Celsius | int | temperature |
| time | `get_time()` | `'HH:MM'` | string | time of report |
| visibility | `visibility()` |  | object | contains visibility data |
| visibility/distance | `get_visibility_distance()` | specified by `visibility/distance_unit` | int | visibility distance |
| visibility/distance_m | `get_visibility_distance_m()` | meters | int or float | converted visibility distance in meters |
| visibility/distance_unit | `get_visibility_distance_unit()` |  | int | unit of visibility distance |
| wind | `wind()` |  | object | contains wind data |
| wind/direction | `get_wind_direction()` | degrees or `'VRB'` | int or string | wind direction |
| wind/gust | `get_wind_gust()` | specified by `wind/speed_unit` | int | gust speed |
| wind/gust_ms | `get_wind_gust_ms()` | meters per second | int or float | converted gust speed in meters per second |
| wind/speed | `get_wind_speed()` | specified by `wind/speed_unit` | int | wind speed |
| wind/speed_ms | `get_wind_speed_ms()` | meters per second | int or float | converted wind speed in meters per second |
| wind/speed_unit | `get_wind_speed_unit()` |  | int | unit of wind speed |
| wind/variable_directions | `get_wind_variable_directions()` | degrees | list | contains variable wind directions |
