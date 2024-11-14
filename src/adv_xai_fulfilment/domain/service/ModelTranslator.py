from ..model.Model import Model
from ..model.machineLearningModel.KerasModel import KerasModel
from ..model.machineLearningModel.TorchModel import TorchModel
from ..model.machineLearningModel.ScikitLearnModel import ScikitLearnModel


class ModelTranslator:
    _framework: str
    _algorithm: str

    def with_(self, framework: str) -> "ModelTranslator":
        self._framework = framework
        return self

    def and_(self, algorithm: str) -> "ModelTranslator":
        self._algorithm = algorithm
        return self

    def translate(self, filename: str) -> Model:
        for model in [KerasModel, TorchModel, ScikitLearnModel]:
            if self._framework.lower() in model.supported_frameworks():
                return model(filename=filename)
