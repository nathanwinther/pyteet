import json
import logging
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pythonjsonlogger.json import JsonFormatter
from smtplib import SMTP
from werkzeug.wrappers import Response

logger = logging.getLogger('pyteet')
logHandler = logging.StreamHandler()
logHandler.setFormatter(JsonFormatter([
    'levelname',
    'message',
    'pathname',
    'lineno',
    ]))
logger.addHandler(logHandler)
logger.setLevel(os.environ.get('PYTEET_LOG_LEVEL', 'ERROR'))

def jsonify(data: any) -> any:
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = jsonify(v)
        return data
    if isinstance(data, list):
        for k, v in enumerate(data):
            data[k] = jsonify(v)
        return data
    if isinstance(data, datetime):
        return data.strftime('%Y-%m-%d %H:%M:%S')
    if hasattr(data, 'for_api'):
        # Handle Model jsonify
        f = getattr(data, 'for_api')
        if callable(f):
            return jsonify(f())
    return data

def parsebool(value: any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ('true', 't', 'yes', 'y', '1')

def parsefloat(value: any) -> float:
    if isinstance(value, float):
        return value
    try:
        return float(str(value).strip())
    except:
        return 0

def parseint(value: any) -> int:
    if isinstance(value, int):
        return value
    try:
        return int(str(value).strip())
    except:
        return 0

def send_json(payload: any, status: int | None=200) -> Response:
    return Response(
            json.dumps(jsonify(payload)),
            mimetype='application/json',
            status=status)

