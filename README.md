# libauspol

![libauspol logo](docs/libauspol_logo_400px.png?raw=true)

A Python library for accessing Australian parliamentary information

## Requirements
 + Python 3.0+
 + BeautifulSoup4
 + requests

## Usage
```python
from auspol.minutes import HouseOfRepsMinutes
from datetime import date

h = HouseOfRepsMinutes()
minutes = h.get_live_minutes()
h.get_minutes(date.today())

```

The `minutes` object has the following format:
```json
[
    {
        "timestamp": datetime,
        "content": "Badly formatted string of the current point",
        "children": {
            "timestamp": datetime,
            "content": "Badly formatted string of a minutes entry",
        },
    }, ...
]
```

## TODO
 + more useful features
