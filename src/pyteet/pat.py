from .database import DATETIME
from .model import Model
from .utils import parseint

import hashlib
import importlib
import json
import secrets
from datetime import datetime
from datetime import UTC
from functools import wraps
from werkzeug.exceptions import Forbidden
from werkzeug.wrappers import Request

class PAT(Model):

    TABLE = 'pyteet_pat'
    PRIMARY_KEY = 'id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    CONNECTION = None # Use default database connection

    @staticmethod
    def has_any(abilities: list):
        '''Decorator to guard routes

        Usage: Route MUST HAVE auth_user=None kwarg

        Example in controller

        @PAT.has_any(['customer'])
        def index(request, auth_user=None)
            pass
        '''
        def has_any_decorate(f):
            @wraps(f)
            def has_any_wrap(*args, **kwargs):
                user = None
                r = None
                # Get request from args
                for arg in args:
                    if isinstance(arg, Request):
                        r = arg
                        break
                user = PAT.auth_user(r, abilities)
                if not user:
                    raise Forbidden
                # Add to kwargs
                kwargs['auth_user'] = user
                # Procced
                return f(*args, **kwargs)
            return has_any_wrap
        return has_any_decorate

    @staticmethod
    def auth_user(request: Request, abilities: list | None=[]) -> Model:
        if not request:
            return None
        if not request.authorization:
            return None
        if request.authorization.type != 'bearer':
            return None
        token = request.authorization.token
        try:
            id, hash_token = token.split('|')
        except:
            return None
        inst = PAT().find(parseint(id))
        if not inst:
            return None
        if inst.get_hash_token() != hash_token:
            return None
        if abilities:
            if not inst.has_any_abilities(abilities):
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
    def create(tokenable: Model, abilities: list) -> PAT:
        inst = PAT()
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
        

    def has_ability(self, ability: str) -> bool:
        inst_abilities = json.loads(self.abilities)
        return ability in inst_abilities

    def has_any_abilities(self, abilities: list) -> bool:
        inst_abilities = json.loads(self.abilities)
        return any(x in abilities for x in inst_abilities)

