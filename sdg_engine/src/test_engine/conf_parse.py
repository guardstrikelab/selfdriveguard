import configparser
import os


def get_conf():
    CONFIG_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'content.ini'))
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    return config
