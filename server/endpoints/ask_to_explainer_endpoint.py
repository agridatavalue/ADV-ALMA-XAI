import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import ExplainerGeneratorPresentation

askToExplainerEndpointBp = Blueprint("ask", __name__)


@askToExplainerEndpointBp.route("/ask", methods=["POST"])
def AskToExplainerEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ExplainerGeneratorPresentation().ask_to_explainer(request.get_json())

        return make_response(
            jsonify({"response": response}),
            200,
        )
    except Exception as e:
        logging.error(f"error while asking to the explainers: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
