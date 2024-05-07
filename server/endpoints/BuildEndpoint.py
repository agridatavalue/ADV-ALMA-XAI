from flask import Blueprint, request, jsonify, make_response

buildBp = Blueprint("build", __name__)

from src.adv_xai_fulfilment.presentation.TrainerPresentation import TrainerPresentation


@buildBp.route("/", methods=["POST"])
def build():
    try:
        response = TrainerPresentation().train(
            request.form.get("model"),
            request.form.get("pilot"),
            request.form.get("metadata"),
        )
        return make_response(
            jsonify(
                {
                    "status": f"success - stored {len(response)} explainers and metadata in SECURESTOR"
                }
            ),
            200,
        )
    except Exception as e:
        return {"status": e}
