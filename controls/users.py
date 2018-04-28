import flask
from exceptions import InvalidUsage, Unauthorized
from database import db
from models import user
import json


user_bp = flask.Blueprint('user', __name__)


@user_bp.route('/user', methods=["POST"])
def sign_up():
    user_info = flask.request.json
    found_user = user.User.find_by_email(user_info['email'])
    if found_user:
        raise InvalidUsage('Account already exists with that email.', status_code=410)
    new_user = user.User()
    new_user.email = user_info['email']
    hashed_pw = ''
    hashed_pw = user.User.generate_hashed_pw(user_info['password'])
    new_user.password = hashed_pw
    new_user.generate_session_token()
    db.session.commit()
    return new_user.serialize()


@user_bp.route('/login', methods=["POST"])
def login():
    user_info = flask.request.json
    found_user = user.User.check_password(user_info["email"], user_info["password"].encode('utf-8'))
    if not found_user:
        raise Unauthorized('Invalid email or password', status_code=401)
    found_user.generate_session_token()
    db.session.commit()
    return found_user.serialize()


@user_bp.route('/session', methods=["POST"])
def session():
    user_info = flask.request.json
    found_user = user.User.find_by_token(user_info['token'])
    if not found_user:
        return json.dumps({"currentUser": None})
    return json.dumps({"currentUser": {
        "id": found_user.id,
        "email": found_user.email,
        "admin": found_user.admin,
        "session_token": found_user.session_token
    }})
