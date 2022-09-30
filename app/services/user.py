"""
    Service abstraction level
    User service class
"""
from string import punctuation
from sqlalchemy.exc import SQLAlchemyError

from .base import BaseService
from app.dao import UserDAO
from app.exceptions import BadRequestData
from app.tools.security import generate_password_hash, compose_passwords, encode_jwt_token, decode_jwt_token
from app.dao.models import User


class UserService(BaseService[UserDAO]):
    def __init__(self, dao: UserDAO):
        self._dao = dao

    @staticmethod
    def calc_password_difficulty(password):
        difficulty: int = 0
        # +1 if great or equal 8 chars
        if len(password) >= 8:
            difficulty += 1
        # +1 if One or more lower case
        difficulty += any(map(str.islower, password))
        # +1 if One or more upper case
        difficulty += any(map(str.isupper, password))
        # +1 if One or more numeric
        difficulty += any(map(str.isdigit, password))
        # +1 if One or more punctuations
        difficulty += any(map(lambda char: char in punctuation, password))

        return difficulty

    @staticmethod
    def create_tokens(user):
        jwt_data = {
            "id": user.id,
            "email": user.email,
        }

        return {
            "access_token": encode_jwt_token(jwt_data, minutes=30),
            "refresh_token": encode_jwt_token(jwt_data, days=100),
        }

    def register(self, data):

        if "email" not in data or "password" not in data:
            raise BadRequestData()

        if self.calc_password_difficulty(data["password"]) < 4:
            raise BadRequestData("Simple password")

        data["password"] = generate_password_hash(data["password"])

        for field in self._dao.__updatable_fields__:
            if field not in data:
                data[field] = None

        return self.create(data)

    def login(self, data):

        if "email" not in data or "password" not in data:
            raise BadRequestData()

        try:
            user = self._dao.get_by_email(data["email"])
        except SQLAlchemyError:
            raise BadRequestData("Invalid user email")

        if user is None:
            raise BadRequestData("Email not found")

        if not compose_passwords(
                generate_password_hash(data["password"]),
                user.password
        ):
            raise BadRequestData("Invalid user password")

        return self.create_tokens(user)

    def refresh(self, refresh_token):
        data = decode_jwt_token(refresh_token)

        if not data or "id" not in data or "email" not in data:
            raise BadRequestData("Invalid refresh token")

        user = self._dao.get_by_id(data["id"])

        if user.email != data["email"]:
            raise BadRequestData("Invalid refresh token")

        return self.create_tokens(user)

    def get(self, data=None):
        if not data or "id" not in data or "email" not in data or "exp" not in data or len(data) != 3:
            raise BadRequestData("Invalid token data")

        user = self.get_item(data["id"])
        if not user or user.email != data["email"]:
            raise BadRequestData("Invalid token data")

        return user

    def patch(self, token_data: dict, data: dict) -> User:

        user = self.get(token_data)

        if not data or "password" in data or "email" in data:
            raise BadRequestData("Invalid patch data")

        return self.partially_update(user.id, data)

    def set_password(self, token_data, data):

        password_1 = data.get("old_password")
        password_2 = data.get("new_password")

        if not password_1 or not password_2:
            BadRequestData("Invalid password data")

        user = self.get(token_data)

        if not compose_passwords(
                generate_password_hash(password_1),
                user.password
        ):
            raise BadRequestData("Invalid user password")

        if self.calc_password_difficulty(password_2) < 4:
            raise BadRequestData("Simple password")

        data = {
            "password": generate_password_hash(password_2)
        }
        return self.partially_update(user.id, data)
