from pyteet.utils import send_json

def index(request):
    return send_json({
        'success': True,
        'message': 'OK',
        })

