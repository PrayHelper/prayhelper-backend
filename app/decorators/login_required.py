import os
from functools import wraps
import jwt
import datetime
from flask import g, request
from app.models.user import User
from app.utils.error_handler import InvalidTokenError


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get("Authorization")
        
        if access_token:
            try:
                payload = jwt.decode(access_token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
                user_id = payload['id']
                access_token_exp = payload['access_token_exp']
                refresh_token_exp = payload['refresh_token_exp']
                if datetime.datetime.fromisoformat(refresh_token_exp) < datetime.datetime.now():
                    raise InvalidTokenError("refresh token expired")
                elif datetime.datetime.fromisoformat(access_token_exp) < datetime.datetime.now():
                    payload = {
                        'id': user_id,
                        'access_token_exp': (datetime.datetime.utcnow() + datetime.timedelta(minutes=60 * 24)).isoformat(),
                        'refresh_token_exp': (datetime.datetime.utcnow() + datetime.timedelta(minutes=60 * 24 * 60)).isoformat()
                    }
                    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
                    return { 'access_token': token }, 200
                else:
                    u = User.query.filter_by(id=user_id).first()
                    if u is not None:
                        g.user_id = user_id
                        g.user = u
                    else:
                        g.user = None
                        raise InvalidTokenError("user not found")
            except jwt.InvalidTokenError:
                raise InvalidTokenError("invalid token")
            return f(*args, **kwargs)
        else:
            raise InvalidTokenError("token not found")
    return decorated_function