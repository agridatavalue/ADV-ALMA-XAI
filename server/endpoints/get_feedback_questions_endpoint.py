from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import QuestionAndFeedbackPresentation

feedbackBp = Blueprint("feedback", __name__)

logger = get_logger()

@feedbackBp.route("/feedback", methods=["POST"])
def get_feedback():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = QuestionAndFeedbackPresentation().get_partner_feedback_from(
            request.get_json()
        )
        
        logger.info("save-feedback successful")
        return make_response(jsonify("OK" if response else "KO"), 200)
    except Exception as e:
        logger.error(f"error while saving the feedback: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
