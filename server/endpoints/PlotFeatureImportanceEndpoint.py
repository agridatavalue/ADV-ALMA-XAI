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
        response: dict[
            "Feature" : list[str],
            "Importance" : list[float],
            "prediction_target":str,
        ] = DataPresentations().genarate_feature_importance(data)

        return make_response(
            jsonify(
                {
                    "values": response.get("Importance", []),
                    "features": response.get("Feature", []),
                    "importance": response.get("prediction_target", ""),
                }
            ),
            200,
        )
    except Exception as e:
        logging.error(f"error while featureimportance: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
