from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import QuestionAndFeedbackPresentation

partnerFeedbackBp = Blueprint("partner_feedback", __name__)

logger = get_logger()

@partnerFeedbackBp.route("/<string:partner>/feedback", methods=["GET"])
def get_partner_feedback(partner:str):
    if request.method != "GET":
        return "Not a valid request"

    try:
        response = QuestionAndFeedbackPresentation().get_provided_partner_feedback(
            {'partner':partner, **request.args}
        )
        
        logger.info("get-partner-feedback successful")
        return make_response(jsonify(response.to_dict() if response else {}), 200)
    except Exception as e:
        logger.error(f"error while getting partner feedback: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
