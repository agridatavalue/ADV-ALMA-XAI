import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.QuestionAndFeedbackPresentation import (
    QuestionAndFeedbackPresentation,
)

questionsBp = Blueprint("questions", __name__)


@questionsBp.route("/feedback", methods=["GET"])
def get_all_questions():
    if request.method != "GET":
        return "Not a valid request"

    metadata: str = request.args.get("metadata")
    logging.info(f"called /feedback api with params {metadata}")
    try:
        response: list = QuestionAndFeedbackPresentation().get_questions_from_metadata(
            metadata_filename=metadata,
        )
        return make_response(
            jsonify(response),
            200,
        )
    except Exception as e:
        logging.error(f"error while getting all questions: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
