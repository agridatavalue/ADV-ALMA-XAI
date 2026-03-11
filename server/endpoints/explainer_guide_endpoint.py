from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ExplainerGeneratorPresentation

explainerGuideBp = Blueprint("explainer_guide", __name__)

logger = get_logger()

@explainerGuideBp.route("/get-explainer-guide", methods=["GET"])
def get_explainer_data_endpoint():
    if request.method != "GET":
        return "Not a valid request"

    try:
        response = ExplainerGeneratorPresentation().get_explainer_guide(
            request.args
        )
        
        logger.info("get-explainer-guide successful")
        return make_response(jsonify(response.to_dict() if response else {}), 200)
    except Exception as e:
        logger.error(f"error while get-explainer-guide the explainers: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
