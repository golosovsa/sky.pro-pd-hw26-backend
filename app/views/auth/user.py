from flask_restx import Namespace, Resource
from flask import request

from app.setup.api.models import user_schema
from app.tools.security import login_required
from app.container import user_service

api = Namespace('user', description="Пользователи")


@api.route("/")
class UserView(Resource):
    @login_required
    @api.marshal_with(user_schema, code=200, description='OK')
    def get(self, token_data):
        answer = user_service.get(token_data)
        return answer

    @login_required
    def patch(self, token_data):
        data = request.json
        user = user_service.patch(token_data, data)
        return "OK", 201


@api.route("/password/")
class UserPasswordView(Resource):
    @login_required
    def put(self, token_data):
        data = request.json
        user_service.set_password(token_data, data)

        return "OK", 201
