from pyteet import \
        config, \
        database_close, \
        Log, \
        parsebool, \
        send_json

import importlib
from werkzeug.exceptions import \
        Forbidden, \
        HTTPException, \
        NotFound
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response

class Router:

    def __init__(self):
        self.routes = Map([])

    def dispatch_request(self, request):
        adapter = self.routes.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return endpoint(request, **values)
        except Forbidden as e:
            return send_json({
                'success': False,
                'message': 'forbidden'}, e.code)
        except NotFound as e:
            return send_json({
                'success': False,
                'message': 'not found'}, e.code)
        except HTTPException as e:
            Log.error(repr(e))
            return send_json({
                'success': False,
                'message': 'server error'}, e.code)
            return e
        finally:
            Log.debug('request cleanup')
            database_close()

    def get(self, pattern, handler):
        self.routes.add(Rule(
            pattern,
            methods=['GET'],
            endpoint=handler))

    def post(self, pattern, handler):
        self.routes.add(Rule(
            pattern,
            methods=['POST'],
            endpoint=handler))

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        if isinstance(response, Response):
            # CORS
            cors = [
                    {'key': 'cors.access_control_allow_origin',
                     'type': str,
                     'header': 'Access-Control-Allow-Origin'},
                    {'key': 'cors.access_control_allow_methods',
                     'type': str,
                     'header': 'Access-Control-Allow-Methods'},
                    {'key': 'cors.access_control_allow_headers',
                     'type': str,
                     'header': 'Access-Control-Allow-Headers'},
                    {'key': 'cors.access_control_allow_credentials',
                     'type': bool,
                     'header': 'Access-Control-Allow-Credentials'},
                    ]
            for item in cors:
                v = config(item['key'])
                if v:
                    if item['type'] == bool:
                        v = parsebool(v)
                    response.headers.update({f'{item['header']}': v})
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

class Route:

    def __init__(self, module_name, handler):
        self.module_name = module_name
        self.handler = handler

    def __call__(self, *args, **kwargs):
        module = importlib.import_module(self.module_name)
        return getattr(module, self.handler)(*args, **kwargs)

