from flask import Flask
from flask_smorest import Api, Blueprint

from src.config.api_config import APIConfig
from src.config.config import Config


def create_app():

    app = Flask(__name__)

    app.config.from_object(APIConfig)

    config = Config().dev_config
    app.env = config.ENV
    
    from src.routes import api
    app.register_blueprint(api, url_prefix = "/api")
    
    return {"app": app, "config": config}