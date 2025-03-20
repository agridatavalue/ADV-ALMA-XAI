import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

from .model_data import ModelData
from .explainers.response_data import PartialDependence
from .explainers.response_data import FeatureDescription
from .machine_learning_model.executors import PartialDependenceExecutor
from .machine_learning_model.executors import IndividualConditionalExpectationsExecutor
from .explainers.response_data import ConfusionMatrix, IndividualConditionalExpectations

class Model:
    name: str
    handler: any
    filename: str

    def __init__(self, filename: str, handler: any = None, name: str = ""):
        self.name = name
        self.handler = handler

        self.filename = filename
        if filename:
            self.load(filename)

    def load(self, path: str) -> "Model": ...

    def is_ok(self) -> bool:
        return self.handler is not None

    @staticmethod
    def supported_frameworks() -> list[str]: ...

    def get_feature_importance(
        self, feature_names: list[FeatureDescription], shap_values: np.array
    ) -> pd.DataFrame: ...

    def __repr__(self) -> str:
        return '{}(name="{}", filename="{}")'.format(
            self.__class__.__name__, self.name, self.filename
        )

    def get_confusion_matrix(self, data: ModelData) -> ConfusionMatrix:
        obj = ConfusionMatrix()
        obj.data = confusion_matrix(data.y, self.handler.predict(data.x))
        return obj

    def get_partial_dependence(self, X: pd.DataFrame, feature: str) -> PartialDependence:
        return PartialDependenceExecutor().process(self, X, feature)
    
    def get_individual_conditional_expectations(self, X: pd.DataFrame, feature: str) -> IndividualConditionalExpectations:
        return IndividualConditionalExpectationsExecutor().process(self, X, feature)
        