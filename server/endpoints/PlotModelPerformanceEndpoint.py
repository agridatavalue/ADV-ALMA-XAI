import json
import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.DataPresentations import DataPresentations

plotModelPerformanceBp = Blueprint("model-performance", __name__)


@plotModelPerformanceBp.route("/model-performance", methods=["POST"])
def plotModelPerformanceEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    data: dict = request.get_json()
    logging.info(f"called /model-performance api with params {data}")
    try:
        response: dict = DataPresentations().genarate_model_performance(
            model_file_name=data.get("model")
        )
        return make_response(
            jsonify(
                {
                    "y_true": json.loads(response.get("y_true").to_json()),
                    "y_pred": response.get("y_pred"),
                }
            ),
            200,
        )
    except Exception as e:
        logging.error(f"error while model-performance: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
