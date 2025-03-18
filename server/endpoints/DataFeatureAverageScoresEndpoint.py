import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import DataPresentations

featureAverageScoresBp = Blueprint("data-features-average-scores", __name__)


@featureAverageScoresBp.route("/data-features-average-scores", methods=["POST"])
def FeatureAverageScoreEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    data: dict = 
    logging.info(f"called /data-features-average-scores api with params {data}")
    try:
        response: dict = DataPresentations().get_features_average_scores(request.get_json())
        return make_response(
            jsonify(response),
            200,
        )
    except Exception as e:
        logging.error(f"error while data-features-average-scores: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
