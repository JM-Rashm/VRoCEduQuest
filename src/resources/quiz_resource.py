from flask.views import MethodView
from flask_smorest import Blueprint

from src.controllers.quiz_controller import QuizController

blp = Blueprint("Quiz", "quiz", description="quiz")

quiz_controller = QuizController()

@blp.route("/qa", methods=["POST", "GET"])
class QuizResouecr(MethodView):
    
    def post(self):
        return quiz_controller.getQAList()
