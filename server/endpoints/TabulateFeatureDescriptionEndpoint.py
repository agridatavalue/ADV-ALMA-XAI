import logging
from flask import Blueprint, jsonify, make_response, request, abort

from src.adv_xai_fulfilment.presentation.DataPresentations import DataPresentations

featureDescriptionEndpointBp = Blueprint("feature_description", __name__)


@featureDescriptionEndpointBp.route("/feature-descriptions", methods=["POST"])
def FeatureDescriptionsEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    data: dict = request.get_json()
    logging.info(f"called /feature-descriptions api with params {data}")
    try:
        response: dict = DataPresentations().genarate_feature_description(
            meta_data_filename=data.get("meta_data")
        )
        return make_response(
            jsonify(
                [
                    {"feature": key, "description": response.get(key)}
                    for key in response.keys()
                ]
            ),
            200,
        )
    except Exception as e:
        logging.error(f"error while featureimportance: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
