from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations

anomalyScoreBp = Blueprint("anomaly-score", __name__)

logger = get_logger()

@anomalyScoreBp.route("/anomaly-score", methods=["POST"])
def build():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ModelDataPresentations().get_anomaly_score(request.get_json())
        
        logger.info("anomaly-score successful")
        return make_response(jsonify(response.to_dict() if response else {}), 200)
    
    except Exception as e:
        logger.error(f"error while anomaly-score: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
