import os
from dotenv import load_dotenv

_config = None


def get_config() -> dict:
    """Read config from env."""
    global _config

    if not _config:
        load_dotenv()
        _config = {}
        _config['API_KEY'] = os.getenv('API_KEY')
        _config['URL'] = os.getenv('URL')
    return _config


