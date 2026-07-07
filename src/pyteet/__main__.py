from pyteet import database_close, Log

import importlib
import sys
from pathlib import Path

def commands(name=None):
    def validate(module):
        must_have = ('NAME', 'DESC', 'run')
        for k in must_have:
            if not hasattr(module, k):
                return False
        return True
    cache = {}
    check = [
            ('pyteet.commands', Path(__file__).resolve().parent / 'commands'),
            ('commands', Path().cwd() / 'commands'),
            ]
    for prefix, path in check:
        if not path.exists():
            #raise ValueError(f'{path.as_posix()} does not exist.')
            continue
        for file in path.iterdir():
            if not file.is_file():
                continue
            if file.suffix != '.py':
                continue
            module_name = f'{prefix}.{file.stem}'
            module = importlib.import_module(module_name)
            if not validate(module):
                continue
            Log.debug(f'pkg module found: {module_name}')
            cache[getattr(module, 'NAME')] = {
                    'NAME': getattr(module, 'NAME'),
                    'DESC': getattr(module, 'DESC'),
                    'module': module_name,
                    }
    return cache.get(name) if name else cache

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 1:
        cache = commands()
        keys = sorted(cache.keys())
        for k in keys:
            print(k)
            print(f'  {cache[k]['DESC']}')
    elif argc > 1:
        cache = commands(sys.argv[1])
        if cache:
            try:
                module = importlib.import_module(cache['module'])
                getattr(module, 'run')(sys.argv[2:])
            except Exception as e:
                raise e
            finally:
                Log.debug('teardown_command')
                database_close()
        else:
            raise ValueError(f'{sys.argv[1]} command not found.')

