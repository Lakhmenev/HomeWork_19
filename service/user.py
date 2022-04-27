import hashlib
import base64
import jwt
from datetime import datetime, timedelta
from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, PWD_HASH_NAME, SECRET_HERE, PWD_HASH_ALGORITHM


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d['password'] = get_hash(user_d['password'])
        return self.dao.create(user_d)

    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)


# Метод хеширование пароля
def get_hash(password):
    hashed_password = hashlib.pbkdf2_hmac(
            hash_name=PWD_HASH_NAME,
            salt=PWD_HASH_SALT.encode('utf-8'),
            iterations=PWD_HASH_ITERATIONS,
            password=password.encode('utf-8'),
            )
    return base64.b64encode(hashed_password).decode('utf-8')

# Метод получения токенов
def generate_tokens(data: dict):
    data['exp'] = datetime.utcnow() + timedelta(minutes=30)
    data['refresh_token'] = False

    access_token = jwt.encode(
        payload=data,
        key=SECRET_HERE,
        algorithm=PWD_HASH_ALGORITHM,
    )

    data['exp'] = datetime.utcnow() + timedelta(days=30)
    data['refresh_token'] = True

    refresh_token: str = jwt.encode(
        payload=data,
        key=SECRET_HERE,
        algorithm=PWD_HASH_ALGORITHM,
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
