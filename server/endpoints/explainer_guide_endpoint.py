import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import ExplainerGeneratorPresentation

explainerGuideBp = Blueprint("explainer_guide", __name__)


@explainerGuideBp.route("/get-explainer-guide", methods=["GET"])
def get_explainer_data_endpoint():
    if request.method != "GET":
        return "Not a valid request"

    try:
        response: list = ExplainerGeneratorPresentation().get_explainer_guide(
            request.args
        )
        return make_response(
            jsonify(
                {
                    "endpoints": [
                        {"url": r.corresponding_endpoint, "name": r.__class__.__name__}
                        for r in response
                    ]
                }
            ),
            200,
        )
    except Exception as e:
        logging.error(f"error while get-explainer-guide the explainers: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
