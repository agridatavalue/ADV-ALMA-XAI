from .explainer_response_data import ExplainerResponseData

class DataDistribution(ExplainerResponseData):
    def __init__(self):
        super().__init__(endpoint='data-distribution')