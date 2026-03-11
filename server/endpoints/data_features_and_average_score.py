from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import ModelDataPresentations

dataFeaturesAvarageScoreBp = Blueprint("data-features-and-average-score", __name__)

logger = get_logger()

@dataFeaturesAvarageScoreBp.route("/data-features-and-average-score", methods=["POST"])
def data_feature_and_average_score():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response = ModelDataPresentations().get_data_features_and_average_score(request.get_json())
        
        logger.info("data-features-and-average-score successful")
        return make_response(jsonify(
            [
                {
                    'feature': feature_name, 
                    'average_score': response.get_average_score_for(feature_name),
                } for feature_name in (response.get_features() if response else [])
            ]), 
            200
        )
    except Exception as e:
        logger.error(f"error while data-features-and-average-score: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
