from models.contact import Contact

import hashlib
from pyteet import PersonalAccessToken, Validator, send_error, send_success

@PersonalAccessToken.auth_has_any(['customer'])
def index(request, auth_user=None):
    return send_success(auth_user.for_api())

def login(request):
    v = Validator()
    v.add('email', Validator.required)
    v.add('email', Validator.email)
    v.add('password', Validator.required)
    ok, field_errors = v.run(request.form)
    if not ok:
        return send_error(field_errors=field_errors)
    user = Contact.login(
            request.form.get('email').strip(),
            request.form.get('password').strip())
    if not user:
        return send_error(
                'Sorry, that email and/or password is invalid!', 401)
    data = user.for_api()
    pat = PersonalAccessToken.create(user, ['customer'])
    data['token'] = pat.bearer()
    return send_success(data)

def register(request):
    def compare(name, value, compare_to=''):
        if str(value).strip() == str(compare_to).strip():
            return True, None
        else:
            return False, 'passwords must match.'
    v = Validator()
    v.add('firstname', Validator.required)
    v.add('lastname', Validator.required)
    v.add('email', Validator.required)
    v.add('email', Validator.email)
    v.add('password', Validator.required)
    v.add('password', 
          compare,
          compare_to=request.form.get('password_compare', ''))
    ok, field_errors = v.run(request.form)
    if not ok:
        return send_error(field_errors=field_errors)
    user = Contact()
    user.firstname = request.form.get('firstname').strip()
    user.lastname = request.form.get('lastname').strip()
    user.email = request.form.get('email').strip()
    user.password = request.form.get('password').strip()
    try:
        user.save()
    except Exception as e:
        return send_error(field_errors={
            'email': [
                'That email address is already in use.',
                ]})
    return send_success(user.for_api())

