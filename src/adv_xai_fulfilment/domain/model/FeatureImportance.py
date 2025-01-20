class FeatureImportance:
    feature: list[str]
    importance: list[float]
    prediction_target: str

    def __init__(
        self, feature: list[str], importance: list[float], prediction_target: str
    ):
        self.feature = feature
        self.importance = importance
        self.prediction_target = prediction_target
