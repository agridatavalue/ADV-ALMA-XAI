from flask import send_file, make_response
from flask import Blueprint, request, jsonify

from logger import get_logger
from src.adv_xai_fulfilment import HelpersPresentation

imageBp = Blueprint("image", __name__)

logger = get_logger()

@imageBp.route("/<string:model>/<string:partner>/image", methods=["GET"])
def get_image(model: str, partner: str):
    if request.method != "GET":
        return "Not a valid request"

    try:
        response = HelpersPresentation().get_image(
            {'partner': partner, 'model': model, **request.args}
        )
        return send_file(response, mimetype="image/jpeg")

    except Exception as e:
        logger.error(f"error while getting image: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
