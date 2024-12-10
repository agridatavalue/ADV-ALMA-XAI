import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.QuestionAndFeedbackPresentation import (
    QuestionAndFeedbackPresentation,
)

feedbackBp = Blueprint("feedback", __name__)


@feedbackBp.route("/feedback", methods=["POST"])
def get_feedback():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response: bool = QuestionAndFeedbackPresentation().get_pilot_feedback_from(
            request.get_json()
        )
        return make_response(
            jsonify("OK" if response else "KO"),
            200,
        )
    except Exception as e:
        logging.error(f"error while saving the feedback: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
