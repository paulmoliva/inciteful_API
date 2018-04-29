import flask
from exceptions import InvalidUsage, Unauthorized
from database import db
from models import category
import json


category_bp = flask.Blueprint('category', __name__)


@category_bp.route('/categories')
def get_all_categories():
    all_categories = category.Category.query.all()
    result = []
    for each_category in all_categories:
        result.append(each_category.as_dict())
    return json.dumps(result)


@category_bp.route('/categories', methods=["POST"])
def create_new_category():
    category_info = flask.request.json
    new_category = category.Category()
    new_category.name = category_info["name"]
    new_category.description = category_info["description"]
    new_category.save()
    db.session.commit()
    return json.dumps({
        "id": new_category.id,
        "name": new_category.name,
        "description": new_category.description
    })
