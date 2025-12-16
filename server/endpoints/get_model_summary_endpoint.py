from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ExplainerGeneratorPresentation

summaryBp = Blueprint("summary", __name__)

logger = get_logger()

@summaryBp.route("<model>/<partner>/get-summary/<language>/", methods=["GET"])
def get_summary(model: str, partner: str, language: str):
    if request.method != "GET":
        return "Not a valid request"

    try:
        response = ExplainerGeneratorPresentation().get_model_summary(
            {**request.args.to_dict(), 'model': model, 'partner': partner, 'language': language}
        )
        return make_response(jsonify(response.to_dict()), 200)
    
    except Exception as e:
        logger.error(f"error while summary: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
