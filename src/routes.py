from flask import Blueprint
from src.resources.quiz_resource import blp as QuizBlueprint

api = Blueprint('api', __name__)

api.register_blueprint(QuizBlueprint, url_prefix="/quiz")