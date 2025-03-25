import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import DataCardPresentations

dataDistributionBp = Blueprint("data-distribution", __name__)


@dataDistributionBp.route("/data-distribution", methods=["POST"])
def DataDistributionEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response: dict = DataCardPresentations().get_data_distribution(request.get_json())
        return make_response(
            jsonify(response),
            200,
        )
    except Exception as e:
        logging.error(f"error while data-distribution: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
