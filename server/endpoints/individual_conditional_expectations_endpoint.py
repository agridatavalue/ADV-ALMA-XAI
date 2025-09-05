from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations

iceBp = Blueprint("ice", __name__)

logger = get_logger()

@iceBp.route("/individual-conditional-expectations", methods=["POST"])
def ice():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ModelDataPresentations().get_individual_conditional_expectations(request.get_json())

        return make_response(jsonify(response.to_dict()), 200)
    except Exception as e:
        logger.error(f"error while individual-conditional-expectations: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
