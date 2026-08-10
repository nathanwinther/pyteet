from models.contact import Contact

from pyteet.pat import PAT
from pyteet.utils import jsonify
from pyteet.utils import send_json
from pyteet.validator import Validator

@PAT.has_any(['customer'])
def index(request, auth_user=None):
    return send_json({
        'success': True,
        'message': 'OK',
        'data': auth_user.for_api(),
        })

def login(request):
    v = Validator()
    v.add('email', v.required)
    v.add('email', v.email)
    v.add('password', v.required)
    ok, field_errors = v.run(request.form)
    if ok:
        contact = Contact.login(
                request.form.get('email').strip(),
                request.form.get('password').strip())
        if contact:
            data = contact.for_api()
            pat = PAT.create(contact, ['customer'])
            data['token'] = pat.bearer()
            return send_json({
                'success': True,
                'message': 'OK',
                'data': data,
                })
        else:
            return send_json({
                'success': False,
                'message': 'Sorry that email and/or password is invalid',
                }, status=400)
    else:
        return send_json({
            'success': False,
            'message': 'Form validation failed',
            'field_errors': field_errors,
            }, status=400)

def register(request):
    v = Validator()
    v.add('email', v.required)
    v.add('email', v.email)
    v.add('password', v.required)
    v.add('firstname', v.required)
    v.add('lastname', v.required)
    ok, field_errors = v.run(request.form)
    if ok:
        contact = Contact()
        contact.fill({
            'email': request.form.get('email').strip(),
            'password': Contact.password_hash(
                request.form.get('password').strip()),
            'firstname': request.form.get('firstname').strip(),
            'lastname': request.form.get('lastname').strip(),
            })
        try:
            contact.save()
            contact = Contact().find(contact.id)
            data = contact.for_api()
            pat = PAT.create(contact, ['customer'])
            data['token'] = pat.bearer()
            return send_json({
                'success': True,
                'message': 'OK',
                'data': data,
                })
        except Exception as e:
            logger.error(repr(e))
            raise e
    else:
        return send_json({
            'success': False,
            'message': 'Form validation failed',
            'field_errors': field_errors,
            }, status=400)
