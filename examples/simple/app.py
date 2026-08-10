from pyteet import Pyteet
from pyteet.config import config
from pyteet.database import database_close
from pyteet.utils import logger
from pyteet.utils import send_json

app = Pyteet(cors_headers=config('cors_headers'))

##############################################################################
# Application Handlers
##############################################################################

@app.errorhandler(401)
def app_unauthorized(e):
    return send_json({
        'success': False,
        'message': 'Unauthorized',
        }, status=e.code)

@app.errorhandler(403)
def app_forbidden(e):
    return send_json({
        'success': False,
        'message': 'Forbidden',
        }, status=e.code)

@app.errorhandler(404)
def app_notfound(e):
    return send_json({
        'success': False,
        'message': 'Not found',
        }, status=e.code)

@app.errorhandler(500)
def app_error(e):
    logger.error(repr(e))
    return send_json({
        'success': False,
        'message': 'Server error',
        }, status=e.code)

@app.postrequesthandler('database')
def postrequesthandler_database():
    database_close()

##############################################################################
# Routes
##############################################################################

app.get('/', 'home/index')
app.post('/api/v1/login', 'account/login')
app.get('/api/v1/me', 'account/index')
app.post('/api/v1/register', 'account/register')

###############################################################################
## Lambda wrapper
###############################################################################

#import awsgi2
#
#def lambda_handler(event, context):
#    return awsgi2.response(app, event, context)

##############################################################################
# Dev server
##############################################################################

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple("127.0.0.1", 5000, app, use_debugger=True, use_reloader=True)
