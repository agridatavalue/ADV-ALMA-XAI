import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import DataPresentations


iceBp = Blueprint("ice", __name__)


@iceBp.route("/individual-conditional-expectations", methods=["POST"])
def ice():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = DataPresentations().get_individual_conditional_expectations(request.get_json())

        return make_response(jsonify(response.to_dict()), 200)
    except Exception as e:
        logging.error(f"error while individual-conditional-expectations: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
