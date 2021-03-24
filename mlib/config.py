import configparser

def ConfigToDict(config_path):
    dictonary = {}
    config = configparser.ConfigParser()
    config.read(config_path)
    sections = config.sections()
    if sections == []:
        return GenerateConfig(config_path)
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
                print("Exception while reading from config file: ", ex)
                dictonary[section][option] = None
    return dictonary

def GenerateConfig(config_path):
    config = configparser.ConfigParser()
    config.read_dict({})
    with open(config_path, 'w') as file:
        config.write(file)
    print('Generated config file, edit it and restart')
    exit()