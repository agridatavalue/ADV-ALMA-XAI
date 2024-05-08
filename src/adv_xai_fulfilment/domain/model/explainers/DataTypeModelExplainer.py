from src.adv_xai_fulfilment.domain.model.models.DataTypeModel import DataTypeModel


class DataTypeModelExplainer:
    data_type: DataTypeModel
    explainer: any

    def __init__(self, data_type: DataTypeModel, explainer: any):
        self.explainer = explainer
        self.data_type = data_type
