import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import DataPresentations

heatmapBp = Blueprint("heatmap", __name__)


@heatmapBp.route("/heatmap", methods=["POST"])
def build():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = DataPresentations().get_heatmap(request.get_json())
        return make_response(
            jsonify({"sources": response.heatmaps}),
            200,
        )
    except Exception as e:
        logging.error(f"error while heatmap: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
