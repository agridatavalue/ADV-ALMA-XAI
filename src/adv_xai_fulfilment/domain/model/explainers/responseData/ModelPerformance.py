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

    def __repr__(self) -> str:
        str_to_return = f"{self.__class__.__name__}("
        for prop in ["target"]:
            if getattr(self, prop):
                str_to_return += f"{prop}={getattr(self, prop)}, "
        return str_to_return + ")"
