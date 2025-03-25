import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import DataPresentations

dataFeaturesAvarageScoreBp = Blueprint("data-features-and-average-score", __name__)


@dataFeaturesAvarageScoreBp.route("/data-features-and-average-score", methods=["POST"])
def data_feature_and_average_score():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = DataPresentations().get_data_features_and_average_score(request.get_json())
        return make_response(jsonify(
            [
                {
                    'feature': feature_name, 
                    'average_score': response.get_average_score_for(feature_name),
                } for feature_name in response.get_features()
            ]), 
            200
        )
    except Exception as e:
        logging.error(f"error while data-features-and-average-score: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
