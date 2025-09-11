from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations

plotModelPerformanceBp = Blueprint("model-performance", __name__)

logger = get_logger()

@plotModelPerformanceBp.route("/model-performance", methods=["POST"])
def plotModelPerformanceEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ModelDataPresentations().genarate_model_performance(request.get_json())
        return make_response(jsonify(response.to_dict()), 200)
    except Exception as e:
        logger.error(f"error while model-performance: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
