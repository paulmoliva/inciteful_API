import flask
from flask import jsonify
import os
from flask_cors import CORS
from models import user
import controls
from database import db
from exceptions import InvalidUsage


application = flask.Flask(__name__)

CORS(application)

application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL') or \
    'mysql+pymysql://cranklogic:cranklogic@127.0.0.1/inciteful'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = os.getenv('SECRET_KEY') or 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Register each controls blueprint
for bp in controls.ALL_BLUEPRINTS:
    application.register_blueprint(bp)

db.init_app(application)


@application.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    application.run(debug=True)
