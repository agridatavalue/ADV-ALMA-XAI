import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import DataPresentations


partialDepBp = Blueprint("part_dep", __name__)


@partialDepBp.route("/partial-dependence", methods=["POST"])
def partial_dependence():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = DataPresentations().get_partial_dependence(request.get_json())

        return make_response(
            jsonify(response.to_dict()),
            200,
        )
    except Exception as e:
        logging.error(f"error while partial dependence: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
