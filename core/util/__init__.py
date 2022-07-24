from core.config import load_database_config, initialize_sqlalchemy_config
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy


def get_orm_instance(app):
    load_database_config(app)
    initialize_sqlalchemy_config(app)

    _db = SQLAlchemy()
    _db.init_app(app)

    return _db
