import os

PYTEET_LOG_LEVEL = os.environ.get('PYTEET_LOG_LEVEL', 'ERROR')

class Log:

    levels = ['SQL', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']

    @staticmethod
    def allow(level: str) -> bool:
        if not level in Log.levels:
            return False
        if not PYTEET_LOG_LEVEL in Log.levels:
            return False
        if Log.levels.index(PYTEET_LOG_LEVEL) > Log.levels.index(level):
            return False
        return True

    @staticmethod
    def debug(message: str | None = None, **kwargs):
        if message:
            kwargs = {'message': message} | kwargs
        Log.log('DEBUG', **kwargs)

    @staticmethod
    def info(message: str | None = None, **kwargs):
        if message:
            kwargs = {'message': message} | kwargs
        Log.log('INFO', **kwargs)

    @staticmethod
    def warn(message: str | None = None, **kwargs):
        if message:
            kwargs = {'message': message} | kwargs
        Log.log('WARN', **kwargs)

    @staticmethod
    def error(message: str | None = None, **kwargs):
        if message:
            kwargs = {'message': message} | kwargs
        Log.log('ERROR', **kwargs)

    @staticmethod
    def fatal(message: str | None = None, **kwargs):
        if message:
            kwargs = {'message': message} | kwargs
        Log.log('FATAL', **kwargs)

    @staticmethod
    def log(level: str, **kwargs):
        if not Log.allow(level):
            return
        data = {'level': level} | kwargs
        print(data)

    @staticmethod
    def sql(message: str | None = None, **kwargs):
        if message:
            kwargs = {'message': message} | kwargs
        Log.log('SQL', **kwargs)


