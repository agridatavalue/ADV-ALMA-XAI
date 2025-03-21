import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import DataPresentations

modelPerformanceMetricsBp = Blueprint("model-performance-metrics", __name__)


@modelPerformanceMetricsBp.route("/model-performance-metrics", methods=["POST"])
def TabulateModelPerformanceMetricsEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = DataPresentations().get_model_performance_metrics(request.get_json())
        return make_response(
            jsonify(
                [{"key": k, "value": response.metrics[k]} for k in response.metrics]
            ),
            200,
        )
    except Exception as e:
        logging.error(f"error while model-performance-metrics: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
