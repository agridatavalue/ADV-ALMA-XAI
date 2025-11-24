from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ExplainerGeneratorPresentation

buildBp = Blueprint("build", __name__)

logger = get_logger()

@buildBp.route("/build", methods=["POST"])
def build():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response: list = ExplainerGeneratorPresentation().build(request.get_json())
        
        logger.info("build explainers successful")
        return make_response(
            jsonify(
                {
                    "status": f"success - stored {len(response)} explainers and metadata in SECURESTOR",
                    "explainers": [{"name": e.file_name} for e in response],
                }
            ),
            200,
        )
    except Exception as e:
        logger.error(
            "Error while building the explainers: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
