from ..DataType import DataType


class DataTypeModelExplainer:
    data_type: DataType
    explainer: any

    def __init__(self, data_type: DataType, explainer: any):
        self.explainer = explainer
        self.data_type = data_type
