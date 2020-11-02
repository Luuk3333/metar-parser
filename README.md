# python-metar-decoder
A METAR decoder written in Python.

## Output format
| **key** | **unit** | **datatype** |
|-|-|-|
| indent | | string
| reported | ISO 8601 | string
| temperatures/temperature | degrees Celsius | int |
| temperatures/dew_point | degrees Celsius | int |
| wind/direction | degrees or `'VRB'` | int or string |
| wind/speed | knots | int |
| wind/gust | knots | int |
| wind/variable/from | degrees | int |
| wind/variable/to | degrees | int |
