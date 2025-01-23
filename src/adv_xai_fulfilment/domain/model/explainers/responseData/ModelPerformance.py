from .ExplainerResponseData import ExplainerResponseData


class ModelPerformance(ExplainerResponseData):

    def __init__(self):
        super().__init__("model-performance")
