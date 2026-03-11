from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations

confusionMatrixBp = Blueprint("confusionMatrix", __name__)

logger = get_logger()

@confusionMatrixBp.route("/confusion-matrix", methods=["POST"])
def confusion_matrix():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ModelDataPresentations().get_confusion_matrix(request.get_json())
        
        logger.info("confusion-matrix successful")
        return make_response(jsonify(response.to_dict() if response else {}), 200)
        
    except Exception as e:
        logger.error(f"error while building the explainers: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
