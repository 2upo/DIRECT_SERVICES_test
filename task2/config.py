from configparser import ConfigParser
import os
import logging

_config = None


def get_config() -> ConfigParser:
    """Read config from .ini file."""
    global _config

    if not _config:
        _config = ConfigParser()
        _config.read(os.path.join(os.path.dirname(__file__), "configuration.ini"))
    return _config["default"]


if __name__ == "__main__":
    # For debug purposes
    logging.warning(list(get_config()["default"].keys()))
