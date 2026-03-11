from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import DataCardPresentations

dataDistributionBp = Blueprint("data-distribution", __name__)

logger = get_logger()

@dataDistributionBp.route("/data-distribution", methods=["POST"])
def DataDistributionEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = DataCardPresentations().get_data_distribution(request.get_json())
        
        logger.info("data-distribution successful")
        return make_response(jsonify(response.to_dict() if response else {}), 200)
    except Exception as e:
        logger.error(f"error while data-distribution: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
