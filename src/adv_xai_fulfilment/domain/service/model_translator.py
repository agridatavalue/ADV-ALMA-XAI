from logger import get_logger
from ..model.model import Model
from ..model.machine_learning_model.keras_model import KerasModel
from ..model.machine_learning_model.torch_model import TorchModel
from ..model.machine_learning_model.scikitlearn_model import ScikitLearnModel

logger = get_logger()

class ModelTranslator:
    _models: list[Model]

    _framework: str
    _algorithm: str

    def __init__(self, models: list[Model] = []) -> None:
        self._models = models or [KerasModel, TorchModel, ScikitLearnModel]

    def with_(self, framework: str) -> "ModelTranslator":
        self._framework = framework
        return self

    def and_(self, algorithm: str) -> "ModelTranslator":
        self._algorithm = algorithm
        return self

    def translate(self, filename: str) -> Model:
        for model in self._models:
            if self._framework.lower() in model.supported_frameworks():
                logger.debug(f"found model for {self._framework}")
                return model(filename=filename)
