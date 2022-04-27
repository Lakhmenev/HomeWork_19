import jwt
from constants import SECRET_HERE, PWD_HASH_ALGORITHM
from flask import request, current_app
from flask_restx import Resource, Namespace, abort

from implemented import auth_dao

protected_ns = Namespace('protected')


def get_token_from_headers(headers: dict):
    if 'Authorization' not in headers:
        abort(401)

    return headers['Authorization'].split(' ')[-1]


def decode_token(token: str, refresh_token: bool = False):
    decoded_token = {}
    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=SECRET_HERE,
            algorithms=[PWD_HASH_ALGORITHM],
        )
    except jwt.PyJWTError:
        current_app.logger.info('Got wrong token "%s"', token)
        abort(401)

    # Проверяем, что это не  refresh_token
    if decoded_token['refresh_token'] != refresh_token:
        abort(400, message='Got wrong token type.')

    return decoded_token


def auth_required(func):
    def wrapper(*args, **kwargs):
        # Получаем заголовок с токеном из запроса.
        token = get_token_from_headers(request.headers)

        # Пытаемся раскодировать токен
        decoded_token = decode_token(token)

        # Проверяем, что пользователь существует.
        if not auth_dao.get_by_username(decoded_token['username']):
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_access_required(func):
    def wrapper(*args, **kwargs):
        # Получаем заголовок с токеном из запроса.
        token = get_token_from_headers(request.headers)

        # Пытаемся раскодировать токен
        decoded_token = decode_token(token)

        if decoded_token['role'] != 'admin':
            abort(403)

        # Проверяем, что пользователь существует.
        if not auth_dao.get_by_username(decoded_token['username']):
            abort(401)

        return func(*args, **kwargs)

    return wrapper


@protected_ns.route('/users')
class UsersView(Resource):
    @auth_required
    def get(self):
        return {}, 200


@protected_ns.route('/admin')
class AdminView(Resource):
    @admin_access_required
    def get(self):
        return {}, 200
