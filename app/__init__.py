from flask import Flask
from app.helpers.app_context import AppContext as AC
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(config_object):
    """
    create_app   creates an instance of the flask app

    Args:
        config_object (string): config file

    """
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # Load config profile
    app.config.from_object(config_object)

    # initiate plugins
    ac = AC()
    ac.db.init_app(app)
    ac.bcrypt.init_app(app)
    ac.jwt.init_app(app)
    # register blueprints
    from app.api import API
    for name in API:
        BP = API[name]
        app.register_blueprint(
            BP['route'], url_prefix=BP['url_prefix'])
    return app
