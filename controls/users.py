import flask
from exceptions import InvalidUsage
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
    new_user.save()
    db.session.commit()
    return json.dumps({'email': new_user.email})
