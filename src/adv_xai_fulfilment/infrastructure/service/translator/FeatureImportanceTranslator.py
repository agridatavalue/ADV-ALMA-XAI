from ....domain.model.explainers.responseData.FeatureImportance import FeatureImportance


class FeatureImportanceTranslator:
    def translate(self, data: dict) -> FeatureImportance:
        return FeatureImportance(
            prediction_target=data.get("prediction_target", ""),
            importance=data.get("importance", {}),
            feature=data.get("feature", {}),
        )
