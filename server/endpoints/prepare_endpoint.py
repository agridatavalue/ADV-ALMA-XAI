import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import ExplainerGeneratorPresentation

prepareBp = Blueprint("prepare", __name__)


@prepareBp.route("/prepare", methods=["POST"])
def prepare():
    if request.method != "POST":
        return "Not a valid request"

    try:

        return make_response(
            jsonify(
                {
                    "status": (
                        "OK"
                        if ExplainerGeneratorPresentation().prepare(request.get_json())
                        else "KO"
                    )
                }
            ),
            200,
        )
    except Exception as e:
        logging.error(f"error while preparing the explainers: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
