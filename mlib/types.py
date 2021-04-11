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

async def aInvalid(*args, **kwargs):
    pass

def Invalid(*args, **kwargs):
    pass
