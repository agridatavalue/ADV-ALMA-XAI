import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import ExplainerGeneratorPresentation

buildBp = Blueprint("build", __name__)


@buildBp.route("/build", methods=["POST"])
def build():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response: list = ExplainerGeneratorPresentation().build(request.get_json())
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
        logging.error(f"error while building the explainers: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
