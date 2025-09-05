import os
from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations

heatmapBp = Blueprint("heatmap", __name__)

logger = get_logger()

@heatmapBp.route("/heatmap", methods=["POST"])
def build():
    if request.method != "POST":
        return "Not a valid request"

    def prepare_path(path: str) -> str:
        """Change the path from a full path to an endpoint path"""
        partial_path = path.replace(os.getenv("TEMP", ""), "")
        return partial_path.replace("data/", 'image?filename=')

    try:
        response = ModelDataPresentations().get_heatmap(request.get_json())
        return make_response(
            jsonify({"sources": [prepare_path(r) for r in response.heatmaps]}),
            200,
        )
    except Exception as e:
        logger.error(f"error while heatmap: {e}: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
