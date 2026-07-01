from models.contact import Contact

from pyteet import NotFound, send_success

def index(request, id):
    c = Contact().find(id)
    if not c:
        raise NotFound()
    return send_success(c.for_api())
