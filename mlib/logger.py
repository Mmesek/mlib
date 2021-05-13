import logging

logging.basicConfig(format="[%(asctime)s] [%(name)10s] [%(levelname)8s] [%(lineno)-4d%(module)8s] %(message)s", datefmt="%m/%d %H:%M:%S")
log = logging.getLogger("mlib")

from . import arguments
arguments.add("--log", default="WARNING", help="Specifies logging level", choices=[i for i in logging._nameToLevel.keys()])
log_level = arguments.parse().log.upper()

log.setLevel(log_level)