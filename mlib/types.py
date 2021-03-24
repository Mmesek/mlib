from enum import Enum

class Enum(Enum):
    def __str__(self):
        return str(self.name)
    def by_str(self, value):
        return self.value
    @classmethod
    def get(cls, value: str):
        '''Usage: class.value_of(str)'''
        try:
            return getattr(cls, str(value), None).value
        except: 
            return
    def __lt__(self, other):
        return self.value < other.value

async def aInvalid(*args, **kwargs):
    pass

def Invalid(*args, **kwargs):
    pass
