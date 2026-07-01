import json
import re
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from werkzeug.wrappers import Response

def camel_to_snake(value):
    value = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', value)
    value = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', value)
    return value.lower()

def parsebool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ('true', 't', 'yes', 'y', '1')

def parsefloat(value):
    if isinstance(value, float):
        return value
    try:
        return float(str(value).strip())
    except:
        return 0

def parseint(value):
    if isinstance(value, int):
        return value
    try:
        return int(str(value).strip())
    except:
        return 0

def render_template(template_name, **context):
    template_path = Path(__file__).resolve().parent / 'templates'
    env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=True)
    t = env.get_template(template_name)
    return t.render(context)

def send_json(data, status=200):
    return Response(
            json.dumps(data),
            mimetype='application/json',
            status=status)

def send_success(data=None, message='OK', meta=None):
    message = message if message else 'OK'
    payload = {'success': True, 'message': message}
    if data:
        payload['data'] = data
    if meta:
        payload['meta'] = meta
    return send_json(payload)

