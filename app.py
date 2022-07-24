from flask import Flask, request, jsonify
from core.config import load_database_config, initialize_sqlalchemy_config
from core.http import deserialize_query_string, ensure_json, handle_http_exception
from core.model import (
    deserialize_entity,
    normalize_entity,
    paginate_multiple,
    paginate_single,
)
from core.model.base import db
from core.model.list_item import ListItem
from core.util import get_orm_instance
from core.validator import validator_factory
from core.validator.rule import Rule
from core.validator.validator import Validator

import os
import core.error as error
import core.http as http
import core.validator.type as data_type

app = Flask(__name__)

load_database_config(app)
initialize_sqlalchemy_config(app)
get_orm_instance(app)


@app.route("/api/list_item", methods={"GET"})
def list_item_all():
    query = deserialize_query_string(request.query_string)

    validator = validator_factory(
        {"page": [data_type.STRING, True], "per_page": [data_type.STRING, True]}
    )

    try:
        validator.validate(query)
    except Exception as e:
        return handle_http_exception(e, http.BAD_REQUEST)

    page = int(query["page"])
    per_page = int(query["per_page"])

    return jsonify(paginate_multiple(ListItem, page, per_page)), http.OK


@app.route("/api/list_item/<id>", methods={"GET"})
def list_item_by_id(id):
    try:
        return jsonify(paginate_single(ListItem, id)), http.OK
    except error.EntityNotFoundError as e:
        return handle_http_exception(e, http.NOT_FOUND)


@app.route("/api/list_item", methods={"POST"})
def create_list_item():
    if not ensure_json(request):
        return (
            jsonify({"message": "Content type must be 'application/json'."}),
            http.UNSUPPORTED_MEDIA_TYPE,
        )

    req = http.json(request)

    validator = validator_factory(
        {
            "thumbnail": [data_type.STRING, True],
            "title": [data_type.STRING, True],
            "attachment_id": [data_type.STRING, True],
            "cond": [data_type.STRING, True],
            "file": [data_type.STRING, True],
            "ind": [data_type.STRING, True],
            "name": [data_type.STRING, True],
            "thumbnail_size": [data_type.STRING, True],
            "amount": [data_type.STRING, True],
            "cate": [data_type.STRING, True],
            "subcate": [data_type.STRING, True],
            "price": [data_type.STRING, True],
            "tags": [data_type.STRING, True],
        }
    )

    try:
        validator.validate(req)
    except Exception as e:
        return handle_http_exception(e, http.BAD_REQUEST)

    list_item = deserialize_entity(ListItem(), req)

    db.session.add(list_item)
    db.session.commit()

    return (
        jsonify(normalize_entity(list_item, ListItem.get_serialization_attribute())),
        http.CREATED,
    )


@app.route("/api/list_item/<id>", methods={"PUT"})
def patch_list_item(id):
    if not ensure_json(request):
        return (
            jsonify({"message": "Content type must be 'application/json'."}),
            http.UNSUPPORTED_MEDIA_TYPE,
        )

    list_item = ListItem.query.filter(ListItem.id == id).first()

    if list_item == None:
        return (
            jsonify({"message": "List item data with id '%s' not found." % (id)}),
            http.NOT_FOUND,
        )

    req = http.json(request)

    validator = validator_factory(
        {
            "thumbnail": [data_type.STRING, False],
            "title": [data_type.STRING, False],
            "attachment_id": [data_type.STRING, False],
            "cond": [data_type.STRING, False],
            "file": [data_type.STRING, False],
            "ind": [data_type.STRING, False],
            "name": [data_type.STRING, False],
            "thumbnail_size": [data_type.STRING, False],
            "amount": [data_type.STRING, False],
            "cate": [data_type.STRING, False],
            "subcate": [data_type.STRING, False],
            "price": [data_type.STRING, False],
            "tags": [data_type.STRING, False],
        }
    )

    try:
        validator.validate(req)
    except Exception as e:
        return handle_http_exception(e, http.BAD_REQUEST)

    list_item = deserialize_entity(list_item, req)

    db.session.flush()
    db.session.commit()

    return (
        jsonify(normalize_entity(list_item, ListItem.get_serialization_attribute())),
        http.OK,
    )


@app.route("/api/list_item/<id>", methods={"DELETE"})
def remove_list_item(id):
    list_item = ListItem.query.filter(ListItem.id == id).first()

    if list_item == None:
        return (
            jsonify({"message": "List item data with id '%s' not found." % (id)}),
            http.NOT_FOUND,
        )

    db.session.delete(list_item)
    db.session.commit()

    return (
        jsonify(
            {
                "id": list_item.id,
                "thumbnail": list_item.thumbnail,
                "title": list_item.title,
                "attachment_id": list_item.attachment_id,
                "cond": list_item.cond,
                "file": list_item.file,
                "ind": list_item.ind,
                "name": list_item.name,
                "thumbnail_size": list_item.thumbnail_size,
                "amount": list_item.amount,
                "cate": list_item.cate,
                "subcate": list_item.subcate,
                "price": list_item.price,
                "tags": list_item.tags,
            }
        ),
        http.OK,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
