from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name

