import bcrypt
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
    def generate_hashed_pw(cls, pw):
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), salt)
        return hashed_pw.decode('utf-8')
