from sklearn.inspection import permutation_importance

from src.adv_xai_fulfilment.domain.model.model import Model
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.machine_learning_model.scikitlearn_model import ScikitLearnModel

from .explainer import Explainer
from ..data_type import DataType
from ..model_data import ModelData
from .datatype_model_explainer import DataTypeModelExplainer


class SklearnPermutationImportanceExplainer(Explainer):
    def __init__(self):
        super().__init__(
            name="SklearnPermutationImportance",
            type=["BlackBox", "Whitebox"],
            categories=["Classification", "Regression"],
            explanations="global",
            is_distributed=False,
            train_set_required=False,
            has_categorical_features=True,
            data_type_explainers=[
                DataTypeModelExplainer(DataType.TABULAR, permutation_importance)
            ],
        )

    def build(self, model, data: ModelData):
        self.build_result = permutation_importance(
            model.handler, 
            data.x_train, 
            data.y_train, 
            random_state = 42
        )
        
    def can_match_with(self, model: Model, meta_data: ModelMetaData) -> bool:
        return (
            super().can_match_with(model, meta_data) 
            and meta_data.framework in ScikitLearnModel.supported_frameworks()
        )
