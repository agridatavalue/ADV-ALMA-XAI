import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import QuestionAndFeedbackPresentation

partnerFeedbackBp = Blueprint("partner_feedback", __name__)


@partnerFeedbackBp.route("/<string:partner>/feedback", methods=["GET"])
def get_partner_feedback(partner:str):
    if request.method != "GET":
        return "Not a valid request"

    try:
        response = QuestionAndFeedbackPresentation().get_provided_partner_feedback(
            {'partner':partner, **request.args}
        )
        return make_response(jsonify(response.to_dict()), 200)
    except Exception as e:
        logging.error(f"error while getting partner feedback: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
