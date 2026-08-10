from pyteet.config import config
from pyteet.utils import send_json

def index(request):
    return send_json({
        'success': True,
        'message': 'OK',
        'data': {
            'name': config('app.name'),
            'environment': config('app.env'),
            },
        })
