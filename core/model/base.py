from flask import Flask
from core.util import get_orm_instance

db = get_orm_instance(Flask(__name__))
