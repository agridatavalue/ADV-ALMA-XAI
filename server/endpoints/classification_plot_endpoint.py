from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations

labelSizesBp = Blueprint("classification-class-label-sizes", __name__)

logger = get_logger()

@labelSizesBp.route("/classification-class-label-sizes", methods=["POST"])
def build():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ModelDataPresentations().get_class_label_sizes(request.get_json())
        
        logger.info("classification-class-label-sizes successful")
        return make_response(jsonify(response.to_dict() if response else {}), 200)
    
    except Exception as e:
        logger.error(f"error while classification-class-label-sizes: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
