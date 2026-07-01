import importlib
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request

class Router:

    def __init__(self):
        self.routes = Map([])

    def dispatch_request(self, request):
        adapter = self.routes.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return endpoint(request, **values)
        except HTTPException as e:
            return e

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

