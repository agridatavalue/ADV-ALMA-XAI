from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ExplainerGeneratorPresentation

askToExplainerEndpointBp = Blueprint("ask", __name__)

logger = get_logger()

@askToExplainerEndpointBp.route("/<string:model>/<string:partner>/ask", methods=["POST"])
def AskToExplainerEndpoint(model: str, partner: str):
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ExplainerGeneratorPresentation().ask_to_explainer(
            {'partner': partner, 'model': model, **request.get_json()}
        )

        logger.info("ask to explainer successful")
        return make_response(jsonify({"response": response}), 200)
    except Exception as e:
        logger.error(f"error while asking to the explainers: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
