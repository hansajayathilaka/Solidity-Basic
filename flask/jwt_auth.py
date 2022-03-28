from functools import wraps
import jwt
from flask import request, abort
from flask import current_app


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "status": False,
                "message": ["Authentication Token is missing!"],
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except Exception as e:
            return {
                "status": False,
                "message": ["Something went wrong"],
                "data": None,
                "error": str(e)
            }, 403

        return f(data, *args, **kwargs)

    return decorated
