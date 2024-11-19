import logging
from flask import Blueprint, jsonify, make_response, request

from src.adv_xai_fulfilment.presentation.DataPresentations import DataPresentations
from src.adv_xai_fulfilment.domain.model.FeatureDescription import FeatureDescription

featureDescriptionEndpointBp = Blueprint("feature_description", __name__)


@featureDescriptionEndpointBp.route("/feature-descriptions", methods=["POST"])
def FeatureDescriptionsEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    try:
        response: list[FeatureDescription] = (
            DataPresentations().genarate_feature_description(request.get_json())
        )
        return make_response(
            jsonify(
                [
                    {"feature": feature.name, "description": feature.description}
                    for feature in response
                ]
            ),
            200,
        )
    except Exception as e:
        logging.error(f"error while featureimportance: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
