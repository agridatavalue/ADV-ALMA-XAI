import os
import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import ModelDataPresentations

heatmapBp = Blueprint("heatmap", __name__)


@heatmapBp.route("/heatmap", methods=["POST"])
def build():
    if request.method != "POST":
        return "Not a valid request"

    def prepare_path(path: str):
        return path.replace(os.getenv("TEMP"), "")

    try:
        response = ModelDataPresentations().get_heatmap(request.get_json())
        return make_response(
            jsonify({"sources": [prepare_path(r) for r in response.heatmaps]}),
            200,
        )
    except Exception as e:
        logging.error(f"error while heatmap: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
