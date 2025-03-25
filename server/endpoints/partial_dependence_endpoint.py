from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations


partialDepBp = Blueprint("part_dep", __name__)

logger = get_logger()

@partialDepBp.route("/partial-dependence", methods=["POST"])
def partial_dependence():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ModelDataPresentations().get_partial_dependence(request.get_json())

        return make_response(
            jsonify(response.to_dict()),
            200,
        )
    except Exception as e:
        logger.error(f"error while partial dependence: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
