from .explainer_response_data import ExplainerResponseData

class DataFeaturesAndAverageScore(ExplainerResponseData):
    _data: dict[str: float]

    def __init__(self):
        super().__init__(endpoint='data-features-and-average-score')
        self._data = {}

    def add_feature(self, name: str, score: float) -> "DataFeaturesAndAverageScore":
        assert isinstance(name, str), f"name must be a string, got {type(name)}"
        assert isinstance(score, float), f"score must be a float, got {type(score)}"
        self._data[name] = score
        return self
    
    def get_features(self) -> list[str]:
        return list(self._data.keys())
    
    def get_average_score_for(self, feature:str) -> float:
        assert isinstance(feature, str), f"feature must be a string, got {type(feature)}"
        return self._data.get(feature)