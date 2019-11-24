from flask import Flask
from app.helper.app_context import AppContext as AC
from app.api import API


def create_app(config_object):
    """
    create_app   creates an instance of the flask app

    Args:
        config_object (string): config file

    """
    app = Flask(__name__)
    # Load config profile
    app.config.from_object(config_object)

    # initiate plugins
    ac = AC()
    ac.db.init_app(app)
    ac.bcrypt.init_app(app)

    # register blueprints
    for name in API:
        BP = API[name]
        app.register_blueprint(
            BP['route'], url_prefix=BP['url_prefix'])
    return app

app = create_app('config.dev')

if __name__ == "__main__":
    app.run(host="0.0.0.0")

from app import middleware