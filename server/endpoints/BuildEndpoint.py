import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.TrainerPresentation import TrainerPresentation

buildBp = Blueprint("build", __name__)


@buildBp.route("/build", methods=["POST"])
def build():
    if request.method != "POST":
        return "Not a valid request"

    logging.info(f"called /build api with params {request.get_json()}")
    try:
        response = TrainerPresentation().train(
            request.get_json().get("model"),
            request.get_json().get("pilot"),
            request.get_json().get("metadata"),
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
        return {"status": e}
