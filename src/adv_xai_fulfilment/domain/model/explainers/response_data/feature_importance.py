from .explainer_response_data import ExplainerResponseData


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

    def get_most_important(self) -> str:
        if not self.feature or not self.importance:
            return ""

        max_index = self.importance.index(max(self.importance))
        return self.feature[max_index]

    def to_dict(self) -> dict:
        return {
            "feature": self.feature if not self.feature.empty else [],
            "importance": self.importance if not self.importance.empty else [],
            "prediction_target": self.prediction_target,
        }

    def __repr__(self) -> str:
        str_to_return = f"{self.__class__.__name__}("
        for prop in ["prediction_target", "feature"]:
            if getattr(self, prop):
                str_to_return += f"{prop}={getattr(self, prop)}, "
        return str_to_return + ")"
