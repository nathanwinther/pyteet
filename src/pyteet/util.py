import json
import re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from werkzeug.wrappers import Response

from .constants import DATETIME

def camel_to_snake(value):
    value = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', value)
    value = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', value)
    return value.lower()


def jsonify(data):
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = jsonify(v)
        return data
    if isinstance(data, list):
        for k, v in enumerate(data):
            data[k] = jsonify(v)
        return data
    if isinstance(data, datetime):
        return data.strftime(DATETIME)
    if hasattr(data, 'for_api'):
        f = getattr(data, 'for_api')
        if callable(f):
            return f(data)
    return data

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


def pluralize(word):
    # Simle pluralize
    # https://www.geeksforgeeks.org/python/python-program-to-convert-singular-to-plural/
    # Check if word is ending with s,x,z or is
    # ending with ah, eh, ih, oh,uh,dh,gh,kh,ph,rh,sh,th
    word = str(word).strip()
    if re.search(r'[sxz]$', word) or re.search(r'[aeioudgkprst]h$', word):
        # Make it plural by adding es in end
        return word + 'es'
    # Check if word is ending with y
    elif re.search(r'y$', word):
        # Make it plural by removing y from end adding ies to end
        return re.sub(r'y$', 'ies', word)
    # In all the other cases
    else:
        # Make the plural of word by adding s in end
        return word + 's'


def render_pyteet_template(template_name, **context):
    template_path = Path(__file__).resolve().parent / 'templates'
    env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=True)
    t = env.get_template(template_name)
    return t.render(context)


def render_template(template_name, **context):
    template_path = Path().cwd() / 'templates'
    env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=True)
    t = env.get_template(template_name)
    return t.render(context)


def send_error(message=None, status=400, field_errors=None):
    message = message if message else 'Oops! That\'s an error'
    payload = {'success': False, 'message': message}
    if field_errors:
        payload['errors'] = field_errors
    else:
        payload['errors'] = []
    return send_json(payload, status)


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

