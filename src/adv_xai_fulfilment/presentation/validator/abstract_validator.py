from src.adv_xai_fulfilment.infrastructure.constants import Errors


class AbstractValidator:
    def _validate_pilot(self, pilot: str) -> bool:
        assert isinstance(pilot, str), Errors.PILOT_NOT_STRING

    def _validate_folder_data(self, data: str) -> bool:
        assert isinstance(data, str), Errors.DATA_FOLDER_NOT_STRING

    def _validate_model(self, model: str) -> bool:
        assert isinstance(model, str), Errors.MODEL_FILENAME_NOT_STRING

    def _validate_metadata(self, metadata: str) -> bool:
        assert isinstance(metadata, str), Errors.METADATA_FILENAME_NOT_STRING

    def _validate_prediction_target_str(self, prediction_target: str) -> bool:
        assert isinstance(prediction_target, str), Errors.PREDICTION_TARGET_NOT_STRING

    def _validate_prediction_target_int(self, prediction_target: int) -> bool:
        assert isinstance(prediction_target, int), Errors.PREDICTION_TARGET_NOT_INT

    def _validate_prediction_targets(self, prediction_targets: list[int]) -> bool:
        assert isinstance(
            prediction_targets, str
        ), Errors.PREDICTION_TARGET_INDEX_NOT_INT

    def _merge_with_default_values(self, new_values:dict) -> dict:
        return {'meta_data':'metadata.json', 'data':'data', **new_values}
