import logging
from flask import send_file, make_response
from flask import Blueprint, request, jsonify

from src.adv_xai_fulfilment import DataPresentations

imageBp = Blueprint("image", __name__)


@imageBp.route("/image", methods=["GET"])
def build():
    if request.method != "GET":
        return "Not a valid request"

    try:
        response = DataPresentations().get_image(request.args)
        return send_file(response, mimetype="image/jpeg")

    except Exception as e:
        logging.error(f"error while getting image: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
