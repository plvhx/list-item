import os


def load_database_config(app):
    app.config["DATABASE_ENGINE"] = os.getenv("DATABASE_ENGINE")
    app.config["DATABASE_HOST"] = os.getenv("DATABASE_HOST")
    app.config["DATABASE_PORT"] = os.getenv("DATABASE_PORT")
    app.config["DATABASE_USER"] = os.getenv("DATABASE_USER")
    app.config["DATABASE_PASSWORD"] = os.getenv("DATABASE_PASSWORD")
    app.config["DATABASE_SCHEMA"] = os.getenv("DATABASE_SCHEMA")


def initialize_sqlalchemy_config(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "%s://%s:%s@%s:%s/%s" % (
        app.config["DATABASE_ENGINE"],
        app.config["DATABASE_USER"],
        app.config["DATABASE_PASSWORD"],
        app.config["DATABASE_HOST"],
        app.config["DATABASE_PORT"],
        app.config["DATABASE_SCHEMA"],
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
