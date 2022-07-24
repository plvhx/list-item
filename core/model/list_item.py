import core.model.base as base


class ListItem(base.db.Model):
    __tablename__ = "list_item"

    id = base.db.Column(base.db.Integer, primary_key=True, autoincrement=True)
    thumbnail = base.db.Column(base.db.String(256), unique=True)
    title = base.db.Column(base.db.String(255), unique=True)
    attachment_id = base.db.Column(base.db.String(128), unique=True)
    cond = base.db.Column(base.db.String(128), unique=True)
    file = base.db.Column(base.db.String(255), unique=True)
    ind = base.db.Column(base.db.Integer, unique=True)
    name = base.db.Column(base.db.String(255), unique=True)
    thumbnail_size = base.db.Column(base.db.String(255), unique=True)
    amount = base.db.Column(base.db.Integer, unique=True)
    cate = base.db.Column(base.db.String(255), unique=True)
    subcate = base.db.Column(base.db.String(255), unique=True)
    price = base.db.Column(base.db.Integer, unique=True)
    tags = base.db.Column(base.db.String(255), unique=True)

    @staticmethod
    def get_serialization_attribute():
        return [
            "id",
            "thumbnail",
            "title",
            "attachment_id",
            "cond",
            "file",
            "ind",
            "name",
            "thumbnail_size",
            "amount",
            "cate",
            "subcate",
            "price",
            "tags",
        ]
