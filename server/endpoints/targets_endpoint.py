from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations

targetsBp = Blueprint("targets", __name__)

logger = get_logger()

@targetsBp.route("/targets", methods=["POST"])
def TargetsEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    logger.info(f"called /targets api with params {data}")
    try:
        response: dict = ModelDataPresentations().get_targets(request.get_json())
        return make_response(
            jsonify(response),
            200,
        )
    except Exception as e:
        logger.error(f"error while targets: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
