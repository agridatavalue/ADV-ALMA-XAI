import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import DataPresentations

confusionMatrixBp = Blueprint("confusionMatrix", __name__)


@confusionMatrixBp.route("/confusion-matrix", methods=["POST"])
def confusion_matrix():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = DataPresentations().get_confusion_matrix(request.get_json())
        
        return make_response(
            jsonify(response.to_dict()),
            200,
        )
    except Exception as e:
        logging.error(f"error while building the explainers: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
