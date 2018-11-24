from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims

from libs.strings import gettext


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": gettext("admin_access_required")}, 401
        else:
            return fn(*args, **kwargs)
    return wrapper
