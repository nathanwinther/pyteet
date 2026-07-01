import os

PYTEET_LOG_LEVEL = os.environ.get('PYTEET_LOG_LEVEL', 'ERROR')
PYTEET_LOG_SQL = os.environ.get('PYTEET_LOG_SQL', '') == '1'

class Log:

    levels = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']

    @staticmethod
    def debug(message=None, **kwargs):
        if message:
            kwargs = {'message': message} | kwargs
        Log.log('DEBUG', **kwargs)

    @staticmethod
    def info(message=None, **kwargs):
        if message:
            kwargs = {'message': message} | kwargs
        Log.log('INFO', **kwargs)

    @staticmethod
    def warn(message=None, **kwargs):
        if message:
            kwargs = {'message': message} | kwargs
        Log.log('WARN', **kwargs)

    @staticmethod
    def error(message=None, **kwargs):
        if message:
            kwargs = {'message': message} | kwargs
        Log.log('ERROR', **kwargs)

    @staticmethod
    def fatal(message=None, **kwargs):
        if message:
            kwargs = {'message': message} | kwargs
        Log.log('FATAL', **kwargs)

    @staticmethod
    def log(level, **kwargs):
        if not level in Log.levels:
            return
        if not PYTEET_LOG_LEVEL in Log.levels:
            return
        if Log.levels.index(PYTEET_LOG_LEVEL) > Log.levels.index(level):
            return
        data = {'level': level} | kwargs
        print(data)

    @staticmethod
    def sql(sql=None, **kwargs):
        if sql:
            kwargs = {'sql': sql} | kwargs
        if PYTEET_LOG_SQL:
            data = {'level': 'SQL'} | kwargs
            print(data)

