from flask import Flask


def init_base_app(name):
    app = Flask(name)

    return app