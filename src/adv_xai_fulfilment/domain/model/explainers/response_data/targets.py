from .explainer_response_data import ExplainerResponseData

class Targets(ExplainerResponseData):
    def __init__(self):
        super().__init__(endpoint='targets')

    def to_dict(self) -> dict:
        return {}