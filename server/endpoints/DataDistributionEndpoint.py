import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.DataPresentations import DataPresentations

dataDistributionBp = Blueprint("data-distribution", __name__)


@dataDistributionBp.route("/data-distribution", methods=["POST"])
def DataDistributionEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    data: dict = request.get_json()
    logging.info(f"called /data-distribution api with params {data}")
    try:
        response: dict = DataPresentations().get_distribution(
            model_filename=data.get("model"),
            meta_data_filename=data.get("meta_data"),
            pilot=data.get("pilot"),
            feature_name=data.get("feature"),
        )
        return make_response(
            jsonify(response),
            200,
        )
    except Exception as e:
        logging.error(f"error while data-distribution: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
