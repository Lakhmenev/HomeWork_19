from dao.model.user import User
from dao.user import UserDAO


class AuthDAO:
    def __init__(self, session):
        self.session = session

    def create(self, data):
        ...

    def get_by_username(self, username):
        users = self.session.query(User)

        if username is not None:
            users = users.filter(User.username == username).all()
            return users
        return None
