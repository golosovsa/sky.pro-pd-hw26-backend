import base64
import datetime
import hashlib
import hmac
import calendar

import jwt
from jwt.exceptions import PyJWTError
from flask import current_app, request, abort


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compose_passwords(password_hash_a: str, password_hash_b: str) -> bool:
    return hmac.compare_digest(
        password_hash_a.encode("utf-8"),
        password_hash_b.encode("utf-8"),
    )


def encode_jwt_token(data, days=0, minutes=30):
    exp_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes, days=days)
    data["exp"] = calendar.timegm(exp_date.timetuple())
    return jwt.encode(
        data,
        current_app.config["SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGORITHM"]
    )


def decode_jwt_token(token: str) -> dict or None:
    try:
        return jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=[current_app.config["JWT_ALGORITHM"]]
        )
    except PyJWTError:
        return None


def login_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        token_data = decode_jwt_token(token)
        if not token_data:
            abort(401)

        kwargs.update({"token_data": token_data})

        return func(*args, **kwargs)

    return wrapper
