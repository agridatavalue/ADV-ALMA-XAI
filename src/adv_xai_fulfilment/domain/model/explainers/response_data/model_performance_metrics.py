import math
from typing import Optional

from .explainer_response_data import ExplainerResponseData


class ModelPerformanceMetrics(ExplainerResponseData):
    metrics: dict

    def __init__(self):
        super().__init__("model-performance-metrics")
        self.metrics = {}

    def add_metric(self, name: str, value: Optional[float]) -> "ModelPerformanceMetrics":
        # assert isinstance(name, str), "Metric name must be a string."
        # assert isinstance(value, (int, float)), "Metric value must be a numeric type."
        
        if isinstance(name, str) and isinstance(value, (int, float)):
            self.metrics[name] = value if not math.isinf(value) else None
        return self

    def has_metrics(self) -> bool:
        return bool(self.metrics)

    def to_dict(self) -> dict:
        return self.metrics

    def __repr__(self) -> str:
        str_to_return = f"{self.__class__.__name__}("
        for prop in []:
            if getattr(self, prop):
                str_to_return += f"{prop}={getattr(self, prop)}, "
        return str_to_return + ")"
