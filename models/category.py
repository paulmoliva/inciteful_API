from models import base_model
from database import db


class Category(db.Model, base_model.BaseModel):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
