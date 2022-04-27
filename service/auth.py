from flask_restx import abort
from dao.auth import AuthDAO
from service.user import get_hash, generate_tokens
# from views.protected import decode_token


class AuthService:

    def __init__(self, dao: AuthDAO):
        self.dao = dao

    def login(self, data: dict):
        user_data = self.dao.get_by_username(data['username'])
        if user_data is None:
            abort(401, message='User not found')

        hash_password = get_hash(data['password'])

        for ind in range(len(user_data)):
            if user_data[ind].password == hash_password:
                tokens: dict = generate_tokens(
                       {
                            'username': data['username'],
                            'role': user_data[ind].role
                        },
                    )
                # print(user_data[ind].role)
                # print(tokens)
                return tokens

        return abort(401, message='Invalid password')

    def get_new_tokens(self, refresh_token: str):

        from views.protected import decode_token
        decoded_token = decode_token(refresh_token, refresh_token=True)

        tokens = generate_tokens(
            data={
                'username': decoded_token['username'],
                'role': decoded_token['role'],
            },
        )
        return tokens
