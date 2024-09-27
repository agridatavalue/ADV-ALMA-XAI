import json
import logging
import pandas as pd
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
        response: pd.DataFrame = DataPresentations().genarate_feature_importance(
            model_file_name=data.get("model"), meta_data_filename=data.get("meta_data")
        )
        response_as_json: dict = json.loads(response.to_json())
        return make_response(
            jsonify(
                {
                    "features": response_as_json.get("Feature", {}).get("0"),
                    "importance": "",
                    "values": [
                        sublist[0]
                        for sublist in response_as_json.get("Importance", {}).get("0")
                    ],
                }
            ),
            200,
        )
    except Exception as e:
        logging.error(f"error while featureimportance: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
