from datetime import timedelta
import re
UNITS = {
    "seconds": ["s", "sec", "second"],
    "month":  ["month"], 
    "minutes": ["m", "min", "minute"], 
    "hours":   ["h", "hour"],
    "days":    ["d", "day"], 
    "weeks":   ["w", "week"], 
    "year":   ["year"]
}
DIGITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
digits = "|".join(f"{i}" for i in DIGITS)
units = "|".join(r"(?P<{}>{})".format(i, "|".join(value)) for i, value in UNITS.items())
TIME_UNITS = re.compile(r"(?i)(?P<value>[\d\.,]+) ?(?P<unit>{})".format(units))

def total_seconds(duration: str) -> timedelta:
    total = timedelta()
    for d in TIME_UNITS.finditer(duration):
        interval, unit = d.group("value"), [i for i in filter(lambda x: x[1], d.groupdict().items())][-1][0]
        interval = interval.replace(',','.')
        if interval == '.':
            continue
        if interval.isalpha():
            interval = DIGITS.index(interval.lower())
        interval = float(interval)
        if unit == 'month':
            interval *= 30
            unit = "days"
        elif unit == "year":
            interval *=365
            unit = "days"
        total += timedelta(**{unit: interval})
    return total
