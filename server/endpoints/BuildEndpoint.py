import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.ExplainerGeneratorPresentation import (
    ExplainerGeneratorPresentation,
)

buildBp = Blueprint("build", __name__)


@buildBp.route("/build", methods=["POST"])
def build():
    if request.method != "POST":
        return "Not a valid request"

    data: dict = request.get_json()
    logging.info(f"called /build api with params {data}")
    try:
        response = ExplainerGeneratorPresentation().build(
            data=data.get("data"),
            pilot=data.get("pilot"),
            modelName=data.get("model"),
            metadata=data.get("metadata"),
            prediction_targets=data.get("prediction_targets", []),
        )
        return make_response(
            jsonify(
                {
                    "status": f"success - stored {len(response)} explainers and metadata in SECURESTOR"
                }
            ),
            200,
        )
    except Exception as e:
        logging.error(f"error while building the explainers: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
