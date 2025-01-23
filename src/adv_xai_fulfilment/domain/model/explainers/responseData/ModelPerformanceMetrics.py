from .ExplainerResponseData import ExplainerResponseData


class ModelPerformanceMetrics(ExplainerResponseData):
    def __init__(self):
        super().__init__("model-performance-metrics")
