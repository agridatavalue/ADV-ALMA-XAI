import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.DataPresentations import DataPresentations

dataSourceBp = Blueprint("data-source", __name__)


@dataSourceBp.route("/data-source", methods=["POST"])
def DataSourceEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    data: dict = request.get_json()
    logging.info(f"called /data-source api with params {data}")
    try:
        response: dict = DataPresentations().get_source_data(
            model_filename=data.get("model"),
            meta_data_filename=data.get("meta_data"),
            pilot=data.get("pilot"),
        )
        return make_response(
            jsonify(response),
            200,
        )
    except Exception as e:
        logging.error(f"error while data-source: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
