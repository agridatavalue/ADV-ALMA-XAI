import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.FeatureImportancePresentation import (
    FeatureImportancePresentation,
)

featureImportanceBp = Blueprint("featureimportance", __name__)


@featureImportanceBp.route("/featureimportance", methods=["POST"])
def featureimportance():
    if request.method != "POST":
        return "Not a valid request"

    data: dict = request.get_json()
    logging.info(f"called /featureimportance api with params {data}")
    try:
        response: dict = FeatureImportancePresentation().genarate_data_for_pilot(
            model_file_name=data.get("model")
        )
        return make_response(jsonify(response), 200)
    except Exception as e:
        logging.error(f"error while featureimportance: {e}")
        return make_response(jsonify({"status": e}))
