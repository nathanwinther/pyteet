import re
from email_validator import validate_email, EmailNotValidError
from pyteet import pluralize

class Validator:

    class ValidatorRule:

        def __init__(self, func, **kwargs):
            self.func = func
            self.kwargs = kwargs

    _rules = {}

    def add_rule(self, name, func, **kwargs):
        if not name in self._rules:
            self._rules[name] = []
        self._rules[name].append(self.ValidatorRule(func, **kwargs))

    def run(self, data):
        ok = True
        errors = {}
        for name, rules in self._rules.items():
            value = data.get(name, '')
            for rule in rules:
                args = [name, value]
                ok, message = rule.func(*args, **rule.kwargs)
                if not ok:
                    ok = False
                    errors[name] = [message]
                    break
        return ok, errors

    @staticmethod
    def email(name, value):
        try:
            validate_email(str(value).strip())
            return True, None
        except:
            return False, f'{name} must be a valid email address.'

    @staticmethod
    def length(name, value, min=None, max=None):
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
    def numeric(name, value):
        try:
            float(str(value).strip())
            return True, None
        except:
            return False, f'{name} must be numeric.'

    @staticmethod
    def regex(name, value, pattern=None):
        if re.search(pattern, str(value).strip()):
            return True, None
        else:
            return False, f'{name} is invalid.'

    @staticmethod
    def required(name, value):
        if str(value).strip():
            return True, None
        else:
            return False, f'{name} is required.'

