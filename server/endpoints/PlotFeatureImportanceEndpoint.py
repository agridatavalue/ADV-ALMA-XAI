import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import DataPresentations

featureImportanceBp = Blueprint("feature-importance", __name__)


@featureImportanceBp.route("/feature-importance", methods=["POST"])
def featureimportance():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = DataPresentations().get_feature_importance(request.get_json())

        return make_response(
            jsonify(
                {
                    "values": response.importance,
                    "features": response.feature,
                    "importance": response.prediction_target,
                }
            ),
            200,
        )
    except Exception as e:
        logging.error(f"error while featureimportance: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
