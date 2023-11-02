import os
import configparser

CONFIG_FILE = os.path.expanduser('~/.magic_commit_config')

def get_api_key():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config.get('DEFAULT', 'api_key', fallback=None)

def set_api_key(api_key):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'api_key': api_key}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
