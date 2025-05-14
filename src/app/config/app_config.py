import configparser
import os

def load_config(config_path=None):
    config = configparser.ConfigParser()
    if config_path is None:
        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, "app.config")
    config.read(config_path)
    return config

def get_section(section_name, config_path=None):
    config = load_config(config_path)
    if section_name in config:
        return dict(config[section_name])
    return {}
