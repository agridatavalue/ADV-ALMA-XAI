from typing import Optional

from logger import get_logger
from ..model.model import Model
from ..model.model_metadata import ModelMetaData
from ..model.machine_learning_model.keras_model import KerasModel
from ..model.machine_learning_model.torch_model import TorchModel
from ..model.machine_learning_model.tabpfn_model import TabpfnModel
from ..model.machine_learning_model.fdml_torch_model import FdmlTorchModel
from ..model.machine_learning_model.scikitlearn_model import ScikitLearnModel
from ..model.machine_learning_model.standalone_xgboost_model import StandaloneXgBoostModel

logger = get_logger()

class ModelTranslator:
    _models: list[Model]
    
    _metadata: ModelMetaData

    def __init__(self, models: list[Model] = []):
        self._models = models or [
            KerasModel, FdmlTorchModel, TorchModel, TabpfnModel, ScikitLearnModel, StandaloneXgBoostModel
        ] # type: ignore

    def with_(self, metadata: ModelMetaData) -> "ModelTranslator":
        self._metadata = metadata
        return self

    def translate(self, filename: str) -> Optional[Model]:
        for model in self._models:
            if (
                self._metadata.framework.lower() in model.supported_frameworks() 
                and (self._metadata.is_federated == model.can_handle_federated())
            ):
                return model(filename=filename, layers=self._metadata.architectures)
        return None
