import logging

class ColorCodes:
    grey = "\x1b[38;21m"
    green = "\x1b[1;32m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[1;34m"
    light_blue = "\x1b[1;36m"
    purple = "\x1b[1;35m"
    reset = "\x1b[0m"

class Formatter(logging.Formatter):
    _colors = {
        logging.DEBUG: ColorCodes.green,
        logging.INFO: ColorCodes.blue,
        logging.WARN: ColorCodes.red,
        logging.ERROR: ColorCodes.yellow
    }
    def format(self, record: logging.LogRecord) -> str:
        def wrap(text: str, color: str):
            return color + text + ColorCodes.reset
        record.levelname = wrap(record.levelname, self._colors.get(record.levelno, ColorCodes.purple))
        return super().format(record)

hndr = logging.StreamHandler()
hndr.setFormatter(Formatter(fmt="[%(asctime)s] [%(name)10s] [%(levelname)16s] [%(lineno)-4d%(module)8s] %(message)s", datefmt="%m/%d %H:%M:%S"))
logging.basicConfig(format="[%(asctime)s] [%(name)10s] [%(levelname)8s] [%(lineno)-4d%(module)8s] %(message)s", datefmt="%m/%d %H:%M:%S", handlers=[hndr])
log = logging.getLogger("mlib")

from . import arguments
arguments.add("--log", default="WARNING", help="Specifies logging level", choices=[i for i in logging._nameToLevel.keys()])
log_level = arguments.parse().log.upper()

log.setLevel(log_level)