import controllers.account

import awsgi2
from flask import Flask, request
from flask_cors import CORS
from pyteet import Log, config, database_close, send_error, send_success

app = Flask(__name__)
CORS(app)

@app.errorhandler(403)
def handle_forbidden(e):
    return send_error('forbidden', 403)

@app.errorhandler(404)
def handle_notfound(e):
    return send_error('not found', 404)

@app.errorhandler(500)
def handle_error(e):
    if hasattr(e, 'original_exception'):
        Log.fatal(repr(e.original_exception))
    return send_error('server error', 500)

@app.teardown_request
def handle_teardown(e=None):
    Log.debug('teardown_request')
    database_close()

##############################################################################
# Routes
##############################################################################

@app.get('/')
def home():
    return send_success({
        'name': config('app.name'),
        'environment': config('app.env'),
        })

@app.post('/api/v1/login')
def api_login():
    return controllers.account.login(request)

@app.post('/api/v1/register')
def api_register():
    return controllers.account.register(request)

@app.get('/api/v1/me')
def api_me():
    return controllers.account.index(request)

##############################################################################
# Lambda wrapper
##############################################################################

def lambda_handler(event, context):
    return awsgi2.response(app, event, context)

