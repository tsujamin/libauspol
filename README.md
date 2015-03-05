# libauspol
A python library for rudimentry Australian Parliment live minutes access.

## requirements
 + python3
 + everything listed in requirements.txt

## usage
```python
from auspol.minutes import HouseOfRepsMinutes
from datetime import date

h = HouseOfRepsMinutes()
minutes = h.get_live_minutes()
h.get_minutes(date.today())

```

the minutes object has the following form
```json
[
    {
        "timestamp": datetime,
        "content": "Badly formated string of the current point",
        "children": {
            "timestamp": datetime,
            "content": "Badly formated string of a minutes entry",
        },
    }, ...
]
```

## todo
 + more useful features
