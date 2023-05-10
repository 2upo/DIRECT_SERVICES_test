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
        _config['DATABASE_PORT'] = os.getenv('DATABASE_PORT')
        _config['POSTGRES_PASSWORD']= os.getenv('POSTGRES_PASSWORD')
        _config['POSTGRES_USER']= os.getenv('POSTGRES_USER')
        _config['POSTGRES_DB']= os.getenv('POSTGRES_DB')
        _config['POSTGRES_HOST']= os.getenv('POSTGRES_HOST')
        _config['POSTGRES_HOSTNAME']= os.getenv('POSTGRES_HOSTNAME')
    return _config


