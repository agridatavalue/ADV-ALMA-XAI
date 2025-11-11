from .explainer_response_data import ExplainerResponseData

class AnomalyVsNormal(ExplainerResponseData):
    def __init__(self):
        super().__init__("anomaly-vs-normal")
        
    def set_data(self, data: list[int]) -> "AnomalyVsNormal":
        self.data = {
            "anomaly_count": data.count(1),
            "normal_count": data.count(0)
        }
        return self
    
    def to_dict(self) -> dict:
        return self.data
        