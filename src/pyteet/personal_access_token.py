import hashlib
import importlib
import json
import secrets
from datetime import datetime, UTC
from flask import Request, request
from functools import wraps
from werkzeug.exceptions import Forbidden

from .constants import DATETIME
from .model import Model
from .util import parseint

class PersonalAccessToken(Model):

    TABLE = 'pyteet_pat'
    PRIMARY_KEY = 'id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    CONNECTION = None # Use default database connection

    @staticmethod
    def auth_has_any(abilities: list):
        '''Decorator to guard routes

        Usage: Route MUST HAVE auth_user=None kwarg

        Example in controller

        @PersonalAccessToken.auth_has_any(['customer'])
        def index(request, auth_user=None)
            pass
        '''
        def auth_has_wrap(f):
            @wraps(f)
            def auth_has_impl(*args, **kwargs):
                user = None
                r = None
                # Has request in args?
                for arg in args:
                    if isinstance(arg, Request):
                        r = arg
                        break
                if not r:
                    # Try using flask request context
                    r = request
                user = PersonalAccessToken.auth_user(r, abilities)
                if not user:
                    raise Forbidden
                # Add to kwargs
                kwargs['auth_user'] = user
                # Procced
                return f(*args, **kwargs)
            return auth_has_impl
        return auth_has_wrap


    @staticmethod
    def auth_user(request: Request, abilities: list | None=[]) -> Model:
        if not request.authorization:
            return None
        if request.authorization.type != 'bearer':
            return None
        token = request.authorization.token
        try:
            id, hash_token = token.split('|')
        except:
            return None
        inst = PersonalAccessToken().find(parseint(id))
        if not inst:
            return None
        if inst.get_hash_token() != hash_token:
            return None
        if abilities:
            if not inst.has_any(abilities):
                return None
        # Record usage
        inst.last_used_at = datetime.now(UTC).strftime(DATETIME)
        inst.save()
        try:
            return inst.get_tokenable()
        except:
            return None


    def bearer(self) -> str:
        return f'{self.id}|{self.get_hash_token()}'


    @staticmethod
    def create(tokenable: Model, abilities: list) -> Model:
        inst = PersonalAccessToken()
        inst.tokenable_module = tokenable.__module__
        inst.tokenable_class = tokenable.__class__.__name__
        inst.tokenable_id = getattr(tokenable, tokenable.PRIMARY_KEY)
        inst.name = 'token'
        inst.token = secrets.token_hex()
        inst.abilities = json.dumps(abilities)
        inst.save()
        return inst


    def get_hash_token(self) -> str:
        return hashlib.sha256(self.token.encode('utf-8')).hexdigest()


    def get_tokenable(self) -> Model:
        model = importlib.import_module(self.tokenable_module)
        class_object = getattr(model, self.tokenable_class)
        return class_object().find(self.tokenable_id)
        

    def has(self, ability: str) -> bool:
        inst_abilities = json.loads(self.abilities)
        return ability in inst_abilities


    def has_any(self, abilities: list) -> bool:
        inst_abilities = json.loads(self.abilities)
        return any(x in abilities for x in inst_abilities)

