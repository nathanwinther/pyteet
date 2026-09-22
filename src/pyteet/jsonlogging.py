import json
import logging
import os

class JsonFormatter(logging.Formatter):
    def format(self, record):
        if record.exc_info:
            tb = record.exc_info[-1]
            stack = []
            while tb:
                stack.append(f'{tb.tb_frame.f_code.co_filename}:{tb.tb_frame.f_lineno}')
                tb = tb.tb_next
            record.msg = {
                    'message': str(record.msg),
                    'exception': record.exc_info[0].__name__,
                    'stack': stack,
                    }
        if isinstance(record.msg, Exception):
            record.msg = str(record.msg)
        return json.dumps({
            "level": record.levelname,
            "message": record.msg,
            "logger": record.name,
            "pathname": record.pathname,
            "lineno": record.lineno,
            })

def getLogger(name: str | None='pyteet') -> logger.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    logger.handlers.clear()
    logger.addHandler(handler)

    return logger

logger = getLogger()

