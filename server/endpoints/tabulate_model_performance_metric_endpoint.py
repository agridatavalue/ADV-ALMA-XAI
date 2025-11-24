from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations

modelPerformanceMetricsBp = Blueprint("model-performance-metrics", __name__)

logger = get_logger()

@modelPerformanceMetricsBp.route("/model-performance-metrics", methods=["POST"])
def TabulateModelPerformanceMetricsEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ModelDataPresentations().get_model_performance_metrics(request.get_json())
        
        logger.info("model-performance-metrics successful")
        return make_response(
            jsonify(
                [{"key": k, "value": response.metrics[k]} for k in response.metrics]
            ),
            200,
        )
    except Exception as e:
        logger.error(f"error while model-performance-metrics: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
