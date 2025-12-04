from flask import Blueprint, request, jsonify, make_response

from logger import get_logger
from src.adv_xai_fulfilment import DataCardPresentations

dataSourceTypesBp = Blueprint("data-source-types", __name__)

logger = get_logger()

@dataSourceTypesBp.route("/data-source-types", methods=["GET"])
def DataSourceTypesEndpoint():
    if request.method != "GET":
        return "Not a valid request"

    try:
        response = DataCardPresentations().get_data_source_types(
            {**request.args, 'model': request.args.get('model', '')}
        )

        logger.info("data-source-types successful")
        return make_response(jsonify({"sources": response.to_dict()}), 200)
    except Exception as e:
        logger.error(f"error while data-source-types: %s - %s", 
            type(e).__name__, 
            str(e),
            exc_info=True
        )
        return make_response(jsonify({"status": str(e)}), 500)
