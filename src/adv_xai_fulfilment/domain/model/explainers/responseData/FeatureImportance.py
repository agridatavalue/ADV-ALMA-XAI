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
        super().__init__("feature-importance")
        self.feature = feature
        self.importance = importance
        self.prediction_target = prediction_target

    def to_dict(self) -> dict:
        return {
            "feature": self.feature,
            "importance": self.importance,
            "prediction_target": self.prediction_target,
        }

    def __repr__(self) -> str:
        str_to_return = f"{self.__class__.__name__}("
        for prop in ["prediction_target", "feature"]:
            if getattr(self, prop):
                str_to_return += f"{prop}={getattr(self, prop)}, "
        return str_to_return + ")"
