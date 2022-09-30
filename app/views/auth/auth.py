from flask_restx import Namespace, Resource
from flask import request

api = Namespace('auth', description="User authentication")

from app.container import user_service


@api.route("/register/")
class AuthRegistrationView(Resource):
    @api.response(400, "Bad request")
    def post(self):
        data = request.json
        user = user_service.register(data)
        return "OK", 201,  {'location': '/users/'}


@api.route("/login/")
class AuthLoginView(Resource):
    @api.response(400, "Bad request")
    def post(self):
        data = request.json
        return user_service.login(data), 201

    @api.response(400, "Bad request")
    def put(self):
        refresh_token = request.form.get("refresh_token", None)
        return user_service.refresh(refresh_token), 201



