try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


def get_config():
    config = {
        '-summary': set(),
    }

    parser = ConfigParser()

    try:
        parser.read('.logboard')
    except IOError:
        return config

    try:
        section = parser['logboard']
    except KeyError:
        return config

    try:
        config['-summary'] = set(filter(None, section['-summary'].split(',')))
    except KeyError:
        pass

    return config
