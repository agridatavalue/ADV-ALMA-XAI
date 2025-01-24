import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import DataPresentations

modelPerformanceMetricBp = Blueprint("model-performance-metric", __name__)


@modelPerformanceMetricBp.route("/model-performance-metric", methods=["POST"])
def TabulateModelPerformanceMetricEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response: dict = DataPresentations().get_model_performance_metric(
            request.get_json()
        )
        return make_response(
            jsonify([{"key": k, "value": response[k]} for k in response.keys()]),
            200,
        )
    except Exception as e:
        logging.error(f"error while model-performance-metric: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
