import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import QuestionAndFeedbackPresentation

questionsBp = Blueprint("questions", __name__)


@questionsBp.route("/feedback", methods=["GET"])
def get_all_questions():
    if request.method != "GET":
        return "Not a valid request"

    try:
        response: list = QuestionAndFeedbackPresentation().get_questions_from_metadata(
            request.args
        )
        return make_response(
            jsonify(response),
            200,
        )
    except Exception as e:
        logging.error(f"error while getting all questions: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
