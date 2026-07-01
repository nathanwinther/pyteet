from pyteet import Route, Router

import awsgi2

app = Router()

app.get('/', Route('controllers.home', 'index'))

def lambda_handler(event, context):
    return awsgi2.response(app, event, context)

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)

