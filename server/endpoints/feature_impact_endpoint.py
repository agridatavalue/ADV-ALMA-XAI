from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations

featureImpactBp = Blueprint("feature-impact", __name__)

logger = get_logger()

@featureImpactBp.route("/feature-impact", methods=["POST"])
def featureimpact():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ModelDataPresentations().get_feature_impact(request.get_json())
        
        logger.info("feature-impact successful")
        return make_response(jsonify(response.to_dict() if response else {}), 200)
    
    except Exception as e:
        logger.error(f"error while feature-impact: %s - %s",
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
