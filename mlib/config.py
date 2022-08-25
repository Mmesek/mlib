import configparser
from typing import Any

def ConfigToDict(config_path, default: dict = {}):
    dictonary = {}
    config = configparser.ConfigParser()
    config.read(config_path)
    sections = config.sections()
    if sections == []:
        return GenerateConfig(config_path, default)
    for section in sections:
        dictonary[section] = {}
        for option in config.options(section):
            try:
                value = config.get(section, option)
                if value.isdigit():
                    value = config.getint(section, option)
                elif value.lower() in ['true', 'false', 'yes', 'no', 'on', 'off']:
                    value = config.getboolean(section, option)
                dictonary[section][option] = value
            except Exception as ex:
                from mlib.logger import log
                log.exception("Exception while reading from config file: ", exc_info=ex)
                dictonary[section][option] = None
    return dictonary

def GenerateConfig(config_path, default: dict = {}):
    config = configparser.ConfigParser()
    config.read_dict(default)
    with open(config_path, 'w') as file:
        config.write(file)
    from mlib.logger import log
    log.exception(f'Generated config file at {config_path}, edit it and restart')
    exit()

# get:
# flags -> .env/config/.yml/.ini -> evironment -> default

CONFIG_PATH = "secrets.ini"
DEFAULT_CONFIG = {}
CONFIG = {}

def load_config(path):
    global CONFIG
    if not CONFIG:
        CONFIG = ConfigToDict(CONFIG_PATH, DEFAULT_CONFIG)
    return CONFIG

def cfg_get(key, default = None, cfg: dict=CONFIG):
    return cfg.get(key, default)

def get(key: str, default: Any, cfg: dict = CONFIG) -> Any:
    """
    Retrieve a key from configuration settings.

    Resolution order for key lookup:
        Flags -> Config file -> Environment -> Default
    
    Parameters
    ----------
    key:
        Key to retrieve
    default:
        Default value
    
    Returns
    -------
    any:
        Boolean, Integer or String
    """
    import os
    from mlib import arguments

    args = vars(arguments.parse_all())
    arg = args.get(key, None)
    if arg is None:
        return arg
    
    arg = cfg_get(key, cfg)
    if arg is None:
        return arg

    return os.getenv(key, default)

def add(key: str, default: Any = None, cfg: dict = DEFAULT_CONFIG) -> bool:
    if key in cfg:
        return False
    cfg[key] = default
    return True

def save(path: str = "config.ini"):
    pass

class Config:
    cfg: dict = {}
    default: dict = {}
    path: str
    def __init__(self, path: str = "config.ini") -> None:
        self.path = path
        self.cfg = ConfigToDict(self.path, self.default)

    def get(self, key: str, default: Any) -> Any:
        return get(key, default, cfg=self.cfg)

    def add(self, key: str, default: Any = None) -> Any:
        return add(key, default, cfg=self.cfg)

    def save(self):
        pass

    def load(self):
        pass

    def set_default(self):
        pass
