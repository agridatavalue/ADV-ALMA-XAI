import numpy as np

from .explainer_response_data import ExplainerResponseData

class FeatureImpact(ExplainerResponseData):
    _data: dict
    
    def __init__(self):
        super().__init__("feature-impact")
        self._data = {}
        
    def with_feature(self, feature_name: str) -> "FeatureImpact":
        self._current_feature = feature_name
        return self
    
    def set_data(self, data: np.ndarray) -> "FeatureImpact":
        self._data[self._current_feature] = data
        return self
    
    def to_dict(self) -> dict:
        return {
            "features": [
                {
                    "name": feature_name,
                    "data": data.tolist() if data is not None else [],
                } for feature_name, data in self._data.items()
            ]
        }

    def __str__(self) -> str:
        return f"FeatureImpact(feature_name={self._data.keys()}, has_data={[d.all() for d in self._data.values()]})"