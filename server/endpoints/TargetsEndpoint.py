import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.DataPresentations import DataPresentations

targetsBp = Blueprint("targets", __name__)


@targetsBp.route("/targets", methods=["POST"])
def TargetsEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    data: dict = request.get_json()
    logging.info(f"called /targets api with params {data}")
    try:
        response: dict = DataPresentations().get_targets(
            model_filename=data.get("model"),
            meta_data_filename=data.get("meta_data"),
            pilot=data.get("pilot"),
        )
        return make_response(
            jsonify(response),
            200,
        )
    except Exception as e:
        logging.error(f"error while targets: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
