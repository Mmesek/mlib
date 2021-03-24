def pick(array: list, amount: int=1) -> list:
    from random import SystemRandom
    sample = SystemRandom().sample
    return [i for i in sample(array, len(array) if amount > len(array) else amount)]

def chance(total: int) -> str:
    try:
        return '{:.3%}'.format(1 / total).replace('.000', '')
    except ZeroDivisionError:
        return ''