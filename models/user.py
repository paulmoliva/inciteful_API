import bcrypt
import json
from database import db
from models import base_model


class User(db.Model, base_model.BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    session_token = db.Column(db.String(255))
    admin = db.Column(db.Boolean)

    @classmethod
    def find_by_email(cls, email):
        found_user = cls.query.filter(cls.email == email).first()
        if found_user:
            return found_user
        return None

    @classmethod
    def find_by_token(cls, token):
        found_user = cls.query.filter(cls.session_token == token).first()
        if found_user:
            return found_user
        return None

    @classmethod
    def generate_hashed_pw(cls, pw):
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), salt)
        return hashed_pw.decode('utf-8')

    @classmethod
    def check_password(cls, email, password):
        found_user = cls.find_by_email(email)
        if not found_user:
            return None
        if bcrypt.checkpw(password, found_user.password.encode('utf-8')):
            return found_user
        return None

    def generate_session_token(self):
        self.session_token = bcrypt.gensalt()
        self.save()

    def serialize(self):
        return json.dumps({
            "id": self.id,
            "email": self.email,
            "admin": self.admin,
            "session_token": self.session_token
        })
