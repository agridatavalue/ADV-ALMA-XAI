import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.ExplainerGeneratorPresentation import (
    ExplainerGeneratorPresentation,
)

buildBp = Blueprint("explainer_data", __name__)


@buildBp.route("/get-explainer-data", methods=["GET"])
def build():
    if request.method != "GET":
        return "Not a valid request"

    try:
        response: dict = ExplainerGeneratorPresentation().get_explainer_data(
            request.args
        )
        return make_response(jsonify(response), 200)
    except Exception as e:
        logging.error(f"error while get-explainer-data the explainers: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
