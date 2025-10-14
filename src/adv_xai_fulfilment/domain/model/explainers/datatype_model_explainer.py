class DataTypeModelExplainer:
    data_type: str
    explainer: object

    def __init__(self, data_type: str, explainer: object):
        self.explainer = explainer
        self.data_type = data_type
