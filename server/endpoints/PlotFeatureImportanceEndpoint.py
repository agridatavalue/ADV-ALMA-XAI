import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.DataPresentations import DataPresentations

featureImportanceBp = Blueprint("feature-importance", __name__)


@featureImportanceBp.route("/feature-importance", methods=["POST"])
def featureimportance():
    if request.method != "POST":
        return "Not a valid request"

    data: dict = request.get_json()
    logging.info(f"called /featureimportance api with params {data}")
    try:
        response = DataPresentations().genarate_feature_importance(
            model_file_name=data.get("model"), meta_data_filename=data.get("meta_data")
        )
        return make_response(jsonify(response.to_json()), 200)
    except Exception as e:
        logging.error(f"error while featureimportance: {e}")
        return make_response(jsonify({"status": e}))
