import hashlib
import importlib
import json
import secrets
from datetime import datetime, UTC
from functools import wraps
from pyteet import DATETIME_DB, Forbidden, Model, parseint, Request

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

        Example

        @PersonalAccessToken.auth_has_any(['customer'])
        def index(request, auth_user=None)
            pass
        '''
        def auth_has_wrap(f):
            @wraps(f)
            def auth_has_impl(*args, **kwargs):
                user = None
                for arg in args:
                    if isinstance(arg, Request):
                        user = PersonalAccessToken.auth_user(arg, abilities)
                        break
                if not user:
                    raise Forbidden
                # Add to kwargs
                kwargs['auth_user'] = user
                # Procced
                return f(*args, **kwargs)
            return auth_has_impl
        return auth_has_wrap

    @staticmethod
    def auth_user(request, abilities=[]):
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
        print(inst.for_api())
        if inst.get_hash_token() != hash_token:
            return None
        if abilities and isinstance(abilities, list):
            if not inst.has_any(abilities):
                return None
        # Record usage
        inst.last_used_at = datetime.now(UTC).strftime(DATETIME_DB)
        inst.save()
        try:
            return inst.get_tokenable()
        except:
            return None

    def bearer(self):
        return f'{self.id}|{self.get_hash_token()}'

    def create(self, tokenable, abilities):
        if not isinstance(tokenable, Model):
            raise ValueError('tokenable must be instance of pyteet.Model')
        if not isinstance(abilities, list):
            raise ValueError('abilities must be a list')
        inst = PersonalAccessToken()
        inst.tokenable_module = tokenable.__module__
        inst.tokenable_class = tokenable.__class__.__name__
        inst.tokenable_id = getattr(tokenable, tokenable.PRIMARY_KEY)
        inst.name = 'token'
        inst.token = secrets.token_hex()
        inst.abilities = json.dumps(abilities)
        inst.save()
        return inst

    def get_hash_token(self):
        return hashlib.sha256(self.token.encode('utf-8')).hexdigest()

    def get_tokenable(self):
        model = importlib.import_module(self.tokenable_module)
        class_object = getattr(model, self.tokenable_class)
        return class_object().find(self.tokenable_id)
        
    def has(self, ability):
        inst_abilities = json.loads(self.abilities)
        return ability in inst_abilities

    def has_any(self, abilities):
        inst_abilities = json.loads(self.abilities)
        return any(x in abilities for x in inst_abilities)

