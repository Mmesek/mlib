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

def replace_multiple(mainString: str, toBeReplaces: list, newString: str) -> str:
    # Iterate over the strings to be replaced
    for elem in toBeReplaces:
        # Check if string is in the main string
        if elem in mainString:
            # Replace the string
            mainString = mainString.replace(elem, newString)

    return mainString

replaceMultiple = replace_multiple

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

def percent_from(value: float, total: float) -> float:
    return (value / total) * 100

def bitflag(flags: int, flag: int) -> bool:
    return flags & flag == flag

def set_bit(result: int, value: int) -> int:
    return result | value

def clear_bit(result: int, value: int) -> int:
    return result & ~value

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

def cap(word: str):
    '''CapitalizedRestINTACT'''
    if word == '':
        return word
    return word[0].upper() + word[1:]

def title_preserving_caps(string, whitespace=' '):
    '''Title PRESERVING CaPS'''
    return whitespace.join(map(cap, string.split(whitespace)))

def cc2jl(my_str):
  """CamelCase to joint_lower"""

  r = my_str[0].lower()
  for i, letter in enumerate(my_str[1:], 1):
    if letter.isupper():
      if my_str[i-1].islower() or (i != len(my_str)-1 and my_str[i+1].islower()):
        r += '_'
    r += letter.lower()
  return r

def cc2jp(my_str):
  """CamelCase to joint_lower_Preserving_Uppercase"""
  my_str = str(my_str)

  r = my_str[0]
  for i, letter in enumerate(my_str[1:], 1):
    if letter.isupper():
      if my_str[i-1].islower() or (i != len(my_str)-1 and my_str[i+1].islower()):
          if my_str[i-1] not in ['_','"',"'"] and my_str[i+1] not in ['_','"',"'"]:
            r += '_'
    r += letter
  return r.strip('_')

from .types import Enum
class Case_Separators(Enum):
    Camel = ""
    Snake = "_"
    Kebab = "-"

    def to(cls, my_str: str):
        return to_case(my_str, cls.value)


def to_case(my_str: str, separator: str) -> str:
    """String to-any_case"""
    return my_str.replace(" ", separator).replace("-", separator).replace("_", separator)

def to_snake(my_str: str) -> str:
    """String to snake_case"""
    return my_str.replace(" ","_").replace("-","_").lower()

def to_kebab(my_str: str) -> str:
    """String to kebab-case"""
    return my_str.replace(" ", "-").replace("_", "-").lower()

def to_camel(my_str: str, default_separator: str="_") -> str:
    """snake_case (or any other by changing default separator) to CamelCase"""
    return "".join(i.title() for i in my_str.split(default_separator))


def try_quote(my_str: str) -> int | str:
    """Attempts to surround input with " unless it's a number in which case it returns integer value"""
    if my_str.startswith('"') and my_str.endswith('"'):
        return my_str
    elif my_str.startswith("'") and my_str.endswith("'"):
        my_str[0] = '"'
        my_str[-1] = '"'
        return my_str
    try:
        return int(my_str)
    except ValueError:
        try:
            int(my_str, 16)
            if "x" not in my_str[:2]:
                raise ValueError
            return my_str
        except ValueError:
            return f'"{my_str}"'

def unquote(my_str: str) -> str:
    """Removes surrounding quotes (" or ')"""
    return my_str.replace('"',"").replace("'","").replace('`', '')

import re

NOT_WORD_OR_DIGIT = re.compile("\W|^(?=\d)")
def clean(my_str) -> str:
    """Replaces any non word characters or digits with underscore"""
    return NOT_WORD_OR_DIGIT.sub("_", my_str)
