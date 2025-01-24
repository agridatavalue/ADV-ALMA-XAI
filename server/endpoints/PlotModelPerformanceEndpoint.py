import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import DataPresentations

plotModelPerformanceBp = Blueprint("model-performance", __name__)


@plotModelPerformanceBp.route("/model-performance", methods=["POST"])
def plotModelPerformanceEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response: dict["target":str, "y_true" : list[float], "y_pred" : list[float]] = (
            DataPresentations().genarate_model_performance(request.get_json())
        )
        return make_response(
            jsonify(
                {
                    "target": response.get("target"),
                    "actual": response.get("y_true"),
                    "predictions": response.get("y_pred"),
                }
            ),
            200,
        )
    except Exception as e:
        logging.error(f"error while model-performance: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
