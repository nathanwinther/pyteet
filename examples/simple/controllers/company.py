from models.company import Company

from pyteet import send_success

def index(request, id):
    c = Company().find(id)
    if not c:
        raise NotFound
    return send_success(c.for_api())
