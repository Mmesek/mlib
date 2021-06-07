def timed(func):
    def inner(*args, **kwargs):
        import time
        sum_seconds = 0.0
        start = time.perf_counter_ns()
        result = func(*args, **kwargs)
        finish = time.perf_counter_ns()
        delta = (finish - start)
        sum_seconds += delta
        print(f"Time for {func.__name__}: {delta}")
        return result
    return inner

def replaceMultiple(mainString: str, toBeReplaces: list, newString: str) -> str:
    # Iterate over the strings to be replaced
    for elem in toBeReplaces:
        # Check if string is in the main string
        if elem in mainString:
            # Replace the string
            mainString = mainString.replace(elem, newString)

    return mainString

def truncate(n: int, decimals: int=0):
    m = 10**decimals
    return int(n * m) / m

def sliceindex(x: str):
    i = 0
    for c in x:
        if c.isalpha():
            i = i + 1
            return i
        i = i + 1

def upperfirst(x: str):
    i = sliceindex(x)
    if i == None:
        return x
    return x[:i].upper() + x[i:]

def grouper(iterable: list, n: int, fillvalue=None):
    from itertools import zip_longest
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def filtr(array: list, regex: str, key: str):
    import re
    pattern = re.compile(regex)
    not_matching = []
    for i in array:
        if pattern.search(i[key]) != None:
            not_matching.append(i)
    return not_matching

def chunks(array: list, max_chunks: int):
    for i in range(0, len(array), max_chunks):
        yield array[i:i+max_chunks]

def total_characters(dictonary: dict):
    total = 0
    t = []
    for i in dictonary.values():
        if type(i) is not int:
            t.append(i)

    for v in t:
        total += len(v)
    return total

from typing import Set
def all_subclasses(cls) -> Set[object]:
    '''Returns all imported subclasses for provided class'''
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])

def percent_of(value: float, percentage: float) -> float:
    return value * (percentage / 100)

def deduce_percentage(value: float, percentage: float) -> float:
    return value - percent_of(value, percentage)

def bitflag(flags: int, flag: int) -> bool:
    return flags & flag == flag

def remove_None(d):
    if type(d) is list:
        _d = []
        for _i in d:
            _d.append(remove_None(_i))
        return _d
    for k, a in d.copy().items():
        if a is None:
            d.pop(k, None)
        elif type(a) is dict:
            d[k] = remove_None(a)
        elif type(a) is list:
            d[k] = [remove_None(i) if type(i) is dict else i for i in a]
    return d