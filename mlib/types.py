from enum import Enum

class Enum(Enum):
    def __str__(self):
        return str(self.name)
    def by_str(self, value):
        return self.value
    @classmethod
    def value_of(cls, value: str):
        '''Get Value of Enum. Usage: class.value_of(str)'''
        try:
            return getattr(cls, str(value), None).value
        except: 
            return
    @classmethod
    def get(cls, value: str):
        '''Get Enum type by value or name'''
        return getattr(cls, str(value), None) or cls(value)

    def __lt__(self, other):
        return self.value < other.value
    def __le__(self, other):
        return self.value <= other.value
    def __gt__(self, other):
        return self.value > other.value
    def __ge__(self, other):
        return self.value >= other.value
    
    @property
    def annotation(cls):
        return cls.__annotations__.get(cls.name, None)

async def aInvalid(*args, **kwargs):
    pass

def Invalid(*args, **kwargs):
    pass

MAGIC_NUMBERS = {
    "apng": (b"acTL", b"IDAT"),
    "png": b"PNG",
    "gif": b"GIF",
    "jpeg": [0xFF, 0xD8, 0xFF, 0xE0],
    "jpeg2": [0xFF, 0xD8, 0xFF, 0xE1],
    "jpg": [0xFF, 0xD8],
    "bmp": b"BM",
    "tiff": [0x49, 0x49, 0x2A],
    "tiff2": [0x4D, 0x4D, 0x2A],
}


def detect_filetype(bytes_to_check: bytes):
    for k, v in MAGIC_NUMBERS.items():
        if type(v) is tuple:
            if all(_ in bytes_to_check for _ in [bytearray(i) for i in v]):
                return k
        elif bytearray(v) in bytes_to_check:
            return k
