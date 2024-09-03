import logging
from flask import Blueprint, request, jsonify, make_response

from src.adv_xai_fulfilment.presentation.DataPresentations import DataPresentations

scatterObservedPredictedEndpointBp = Blueprint("plot_scatter", __name__)


@scatterObservedPredictedEndpointBp.route("/plot_scatter", methods=["POST"])
def PlotScatterObservedPredictedEndpoint():
    if request.method != "POST":
        return "Not a valid request"

    data: dict = request.get_json()
    logging.info(f"called /plot_scatter api with params {data}")
    try:
        response: dict = DataPresentations().genarate_performance_scatter_plot(
            model_file_name=data.get("model")
        )
        return make_response(jsonify(response), 200)
    except Exception as e:
        logging.error(f"error while featureimportance: {e}")
        return make_response(jsonify({"status": str(e)}), 500)
