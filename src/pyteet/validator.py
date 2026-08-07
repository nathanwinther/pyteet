import re
from collections.abc import Callable
from email_validator import validate_email

class Validator:

    class ValidatorRule:

        def __init__(self, func, **kwargs):
            self.func = func
            self.kwargs = kwargs

    def __init__(self):
        self._rules = {}

    def add(self, name: str, func: Callable, **kwargs):
        if not name in self._rules:
            self._rules[name] = []
        self._rules[name].append(self.ValidatorRule(func, **kwargs))

    def run(self, data: dict) -> bool, dict:
        ok = True
        errors = {}
        for name, rules in self._rules.items():
            value = data.get(name, '')
            for rule in rules:
                args = [name, value]
                _ok, message = rule.func(*args, **rule.kwargs)
                if not _ok:
                    ok = False
                    errors[name] = [message]
                    break
        return ok, errors

    @staticmethod
    def email(name: str, value: any) -> bool:
        try:
            validate_email(str(value).strip())
            return True, None
        except:
            return False, f'{name} must be a valid email address.'

    @staticmethod
    def length(name: str, value: any, min:int | None=None, max:int | None=None) -> bool:
        value = str(value).strip()
        if min:
            if len(value) >= min:
                return True, None
            else:
                return False, f'{name} must have minimum {min} characters.'
        if max:
            if len(value) <= max:
                return True, None
            else:
                return False, f'{name} must have maximum {max} characters.'
        return True, None
        
    @staticmethod
    def numeric(name: str, value: str) -> bool:
        try:
            float(str(value).strip())
            return True, None
        except:
            return False, f'{name} must be numeric.'

    @staticmethod
    def regex(name: str, value: any, pattern: str | None=None) -> bool:
        if re.search(pattern, str(value).strip()):
            return True, None
        else:
            return False, f'{name} is invalid.'

    @staticmethod
    def required(name: str, value: any) -> bool:
        if str(value).strip():
            return True, None
        else:
            return False, f'{name} is required.'

