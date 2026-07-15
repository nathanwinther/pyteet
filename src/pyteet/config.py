import configparser
from pathlib import Path

from .log import Log

_config = {}

def config(name: str | None = None, default: any | None = None) -> str:
    def load_config():
        Log.debug(message='load config')
        path = Path().cwd() / 'app.ini'
        if not path.exists():
            raise ValueError(f'{path.as_posix()} does not exist.')
        cfg = configparser.ConfigParser()
        cfg.read(path.as_posix())
        for section in cfg.sections():
            if not section in _config:
                _config[section] = {}
            for k, v in cfg[section].items():
                _config[section][k] = v

    if not _config:
        load_config()

    if not name:
        return _config

    parts = name.split('.')
    section = parts.pop(0)
    key = '.'.join(parts)

    if not section in _config:
        return default

    if key:
        return _config[section].get(key, default)

    return _config[section]

