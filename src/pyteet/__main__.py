from .command import get_commands
from .database import database_close

import sys

if __name__ == '__main__':
    commands = get_commands()

    argc = len(sys.argv)
    if argc == 1:
        keys = sorted(commands.keys())
        for k in keys:
            print(k)
            print(f'  {commands[k].DESC}')
    elif argc == 2 and sys.argv[1] == '-h':
        keys = sorted(commands.keys())
        for k in keys:
            print(k)
            print(f'  {commands[k].DESC}')
    elif argc > 1:
        cmd = commands.get(sys.argv[1])
        if cmd:
            try:
                cmd(sys.argv[2:])
            except Exception as e:
                raise e
            finally:
                database_close()
        else:
            print(f'{sys.argv[1]} command not found.')

