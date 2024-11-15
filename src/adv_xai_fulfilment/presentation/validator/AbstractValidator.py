from src.adv_xai_fulfilment.infrastructure.Constants import Errors


class AbstractValidator:
    def _validate_pilot(self, pilot: str) -> bool:
        assert isinstance(pilot, str), Errors.PILOT_NOT_STRING

    def _validate_model(self, model: str) -> bool:
        assert isinstance(model, str), Errors.MODEL_FILENAME_NOT_STRING

    def _validate_metadata(self, metadata: str) -> bool:
        assert isinstance(metadata, str), Errors.METADATA_FILENAME_NOT_STRING

    def _validate_prediction_target(self, prediction_target: str) -> bool:
        assert isinstance(prediction_target, str), Errors.PREDICTION_TARGET_NOT_STRING
