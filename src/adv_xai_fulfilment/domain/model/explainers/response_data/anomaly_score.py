import pandas as pd

class AnomalyScore:
    _data: pd.DataFrame
    
    def __init__(self, data: pd.DataFrame):
        self._data = data
    
    @staticmethod
    def from_data(data: pd.DataFrame) -> "AnomalyScore":
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame")
        
        return AnomalyScore(data)
    
    def assign_scores(self, scores: list[float]) -> "AnomalyScore":
        if len(scores) != len(self._data):
            raise ValueError(
                f"Length of scores {len(scores)} must match number of data points {self._data.shape[0]}"
            )
            
        self._data['scores'] = scores
        return self
    
    def to_dict(self) -> dict:
        return self._data.to_dict(orient='records')