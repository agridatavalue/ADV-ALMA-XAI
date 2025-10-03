from src.adv_xai_fulfilment.infrastructure.constants import Errors


class AbstractValidator:
    def _validate_partner(self, partner: str) -> bool:
        if not isinstance(partner, str):
            raise TypeError(Errors.PARTNER_NOT_STRING)
        if not partner:
            raise ValueError(Errors.PARTNER_NOT_EMPTY)
        return True

    def _validate_feature(self, feature: str) -> bool:
        if not isinstance(feature, str):
            raise TypeError(Errors.FEATURE_NOT_STRING)
        if not feature:
            raise ValueError(Errors.FEATURE_NOT_EMPTY)
        return True

    def _validate_model(self, model: str) -> bool:
        if not isinstance(model, str):
            raise TypeError(Errors.MODEL_FILENAME_NOT_STRING)
        return True

    def _validate_metadata(self, metadata: str) -> bool:
        if not isinstance(metadata, str):
            raise TypeError(Errors.METADATA_FILENAME_NOT_STRING)
        return True

    def _validate_prediction_target_str(self, prediction_target: str) -> bool:
        if not isinstance(prediction_target, str):
            raise TypeError(Errors.PREDICTION_TARGET_NOT_STRING)
        return True

    def _validate_prediction_target_int(self, prediction_target: int) -> bool:
        if not isinstance(prediction_target, int):
            raise TypeError(Errors.PREDICTION_TARGET_NOT_INT)
        return True

    def _validate_prediction_targets(self, prediction_targets: list[int]) -> bool:
        if not isinstance(prediction_targets, list):
            raise TypeError(Errors.PREDICTION_TARGETS_NOT_LIST)
        return True

    def _merge_with_default_values(self, new_values: dict) -> dict:
        return {
            'data_for_train': 'data_train', 
            'data_for_predict': 'data', 
            'meta_data': 'metadata.json', 
            **new_values
        }
