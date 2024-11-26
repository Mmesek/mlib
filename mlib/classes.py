class Mixin:
    def __init_subclass__(cls, *args, using, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        using.__dict__.update(cls.__dict__)


def reopen(cls):
    def dec(mixin):
        for name, obj in vars(mixin).items():
            setattr(cls, name, obj)

    return dec
