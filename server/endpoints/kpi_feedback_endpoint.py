from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import KpiDataPresentation

kpiFeedbackBp = Blueprint("kpi-feedback", __name__)

logger = get_logger()

@kpiFeedbackBp.route("/kpi/feedback/<model>", methods=["GET"])
def kpi_feedback(model: str):
    if request.method != "GET":
        return "Not a valid request"

    try:
        response: dict = KpiDataPresentation().get_model_feedback(
            {**request.args.to_dict(), 'model': model}
        )
        return make_response(jsonify(response), 200)
    
    except Exception as e:
        logger.error(f"error while kpi/feedback: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
