import json
import os
from datetime import date
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from werkzeug.wrappers import Response

def jsonify(data: any) -> any:
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = jsonify(v)
        return data
    if isinstance(data, list):
        for k, v in enumerate(data):
            data[k] = jsonify(v)
        return data
    if isinstance(data, date):
        return data.isoformat()
    if isinstance(data, datetime):
        return data.isoformat()
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

def send_html(html: str, status: int | None=200) -> Response:
    return Response(
            html,
            mimetype='text/html',
            status=status)

def send_json(payload: any, status: int | None=200) -> Response:
    return Response(
            json.dumps(jsonify(payload)),
            mimetype='application/json',
            status=status)

