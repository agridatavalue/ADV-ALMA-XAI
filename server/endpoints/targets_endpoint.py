from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import DataCardPresentations

targetsBp = Blueprint("targets", __name__)

logger = get_logger()

@targetsBp.route("/targets", methods=["POST"])
def TargetsEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = DataCardPresentations().get_targets(request.get_json())
        return make_response(jsonify(response.to_dict()), 200)
    
    except Exception as e:
        logger.error(f"error while targets: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
