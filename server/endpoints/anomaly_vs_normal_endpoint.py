from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations

anomalyVsNormalBp = Blueprint("anomaly-vs-normal", __name__)

logger = get_logger()

@anomalyVsNormalBp.route("/anomaly-vs-normal", methods=["POST"])
def build():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ModelDataPresentations().get_anomaly_vs_normal(request.get_json())
        
        logger.info("anomaly-vs-normal successful")
        return make_response(jsonify(response.to_dict()), 200)
    
    except Exception as e:
        logger.error(f"error while anomaly-vs-normal: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
