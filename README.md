# libauspol
A python library for rudimentry Australian Parliment live minutes access.

## requirements
 + python3
 + everything listed in requirements.txt

## usage
```python
from auspol.minutes import HouseOfRepsMinutes
h = HouseOfRepsMinutes()
minutes = h.get_minutes()
```

the minutes object has the following form
```json
[
    {
        "timestamp": struct_time,
        "content": "Badly formated string of the current point",
        "children": {
            "timestamp": struct_time,
            "content": "Badly formated string of a minutes entry",
        },
    }, ...
]
```

## todo
 + add the federation chamber
 + add date-awareness
 + more useful features
