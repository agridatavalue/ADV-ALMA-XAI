from .ExplainerResponseData import ExplainerResponseData


class FeatureImportance(ExplainerResponseData):
    feature: list[str]
    importance: list[float]
    prediction_target: str

    def __init__(
        self,
        prediction_target: str,
        feature: list[str] = [],
        importance: list[float] = [],
    ):
        self.feature = feature
        self.importance = importance
        self.prediction_target = prediction_target

    def to_dict(self) -> dict:
        return {
            "feature": self.feature,
            "importance": self.importance,
            "prediction_target": self.prediction_target,
        }
