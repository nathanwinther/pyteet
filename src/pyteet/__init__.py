# SPDX-FileCopyrightText: 2026-present Nathan Winther <nathanwinther@fastmail.fm>
#
# SPDX-License-Identifier: MIT

import json
import importlib
from datetime import datetime
from werkzeug.datastructures import Headers
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map
from werkzeug.routing import Rule
from werkzeug.wrappers import Request
from werkzeug.wrappers import Response

class Pyteet:

    def __init__(self, cors_headers=None):
        self.cors_headers = cors_headers
        self.url_map = Map()
        self.errorhandlers = {}

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def dispatch_request(self, request):
        if request.method == 'OPTIONS':
            response = Response(status=204)
            if self.cors_headers:
                response.headers.extend(self.cors_headers)
            return response

        adapter = self.url_map.bind_to_environ(request.environ)

        try:
            endpoint, values = adapter.match()
            segments = endpoint.split('/')
            handler = segments.pop()
            module = importlib.import_module('.'.join(['controllers'] + segments))
            response = getattr(module, handler)(request, **values)
            if self.cors_headers:
                response.headers.extend(self.cors_headers)
            return response
        except HTTPException as e:
            handler = self.errorhandlers.get(str(e.code))
            if handler:
                return handler(e)
            return e

    def errorhandler(self, code: int):
        def decorate(f):
            self.errorhandlers[str(code)] = f
            return f
        return decorate

    def get(self, string, endpoint):
        self.url_map.add(Rule(string, endpoint=endpoint, methods=['GET']))

    def post(self, string, endpoint):
        self.url_map.add(Rule(string, endpoint=endpoint, methods=['POST']))

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

