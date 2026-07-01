from pyteet import config, send_success

def index(request):
    return send_success(meta={
        'name': config('app.name'),
        'environment': config('app.env'),
        })
