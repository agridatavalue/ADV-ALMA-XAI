from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations

liftcurveBp = Blueprint("lift-curve", __name__)

logger = get_logger()

@liftcurveBp.route("/lift-curve", methods=["POST"])
def lift_curve():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ModelDataPresentations().get_lift_curve(request.get_json())
        
        logger.info("lift-curve successful")
        return make_response(jsonify(response.to_dict() if response else {}), 200)
    
    except Exception as e:
        logger.error(f"error while building the explainers: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
