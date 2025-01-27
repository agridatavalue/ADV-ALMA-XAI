from .ExplainerResponseData import ExplainerResponseData


class ModelPerformanceMetrics(ExplainerResponseData):
    metrics: dict

    def __init__(self):
        super().__init__("model-performance-metrics")
        self.metrics = {}

    def add_metric(self, name: str, value: float) -> "ModelPerformanceMetrics":
        assert isinstance(name, str), "Metric name must be a string."
        assert isinstance(value, (int, float)), "Metric value must be a numeric type."

        self.metrics[name] = value
        return self
