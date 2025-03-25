import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment import DataCardPresentations

dataSourceTypesBp = Blueprint("data-source-types", __name__)


@dataSourceTypesBp.route("/data-source-types", methods=["GET"])
def DataSourceTypesEndpoint():
    if request.method != "GET":
        return "Not a valid request"

    try:
        response: dict = DataCardPresentations().get_data_source_types(request.args)

        return make_response(
            jsonify(response),
            200,
        )
    except Exception as e:
        logging.error(f"error while data-source-types: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
