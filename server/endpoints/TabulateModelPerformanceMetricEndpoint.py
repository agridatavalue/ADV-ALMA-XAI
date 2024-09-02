import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.DataPresentations import DataPresentations

modelPerformanceMetricBp = Blueprint("model-performance-metric", __name__)


@modelPerformanceMetricBp.route("/model-performance-metric", methods=["POST"])
def TabulateModelPerformanceMetricEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    data: dict = request.get_json()
    logging.info(f"called /model-performance-metric api with params {data}")
    try:
        response = DataPresentations().get_model_performance_metric(
            model_filename=data.get("model")
        )
        return make_response(
            jsonify({"response": response}),
            200,
        )
    except Exception as e:
        logging.error(f"error while model-performance-metric: {e}")
        return make_response(jsonify({"status": e}))
