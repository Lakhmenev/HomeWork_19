from flask_restx import Resource, Namespace
from implemented import auth_service
from flask import request

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        return auth_service.login(request.json)

    def put(self):
        return auth_service.get_new_tokens(request.json['refresh_token'])
