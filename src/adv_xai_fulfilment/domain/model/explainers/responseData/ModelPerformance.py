from .ExplainerResponseData import ExplainerResponseData


class ModelPerformance(ExplainerResponseData):
    target: str
    y_true: list[float]
    y_pred: list[float]

    def __init__(
        self, target: str = "", y_true: list[float] = [], y_pred: list[float] = []
    ):
        super().__init__("model-performance")
        self.target = target
        self.y_true = y_true
        self.y_pred = y_pred
