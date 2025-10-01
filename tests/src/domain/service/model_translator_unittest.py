import unittest

from src.adv_xai_fulfilment.domain.service import ModelTranslator
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.machine_learning_model.keras_model import KerasModel
from src.adv_xai_fulfilment.domain.model.machine_learning_model.torch_model import TorchModel
from src.adv_xai_fulfilment.domain.model.machine_learning_model.scikitlearn_model import ScikitLearnModel


class SilentKerasModel(KerasModel):
    def load(self, data: dict) -> "KerasModel":
        return self


class SilentTorchModel(TorchModel):
    def load(self, data: dict) -> "TorchModel":
        return self


class SilentScikitLearnModel(ScikitLearnModel):
    def load(self, data: dict) -> "ScikitLearnModel":
        return self


class TestModelTranslator(unittest.TestCase):
    def test_translate(self):
        testObj = ModelTranslator(
            models=[
                SilentKerasModel,
                SilentTorchModel,
                SilentScikitLearnModel,
            ]
        )
        
        self.assertIsInstance(
            testObj.with_(
                metadata=ModelMetaData(
                    data_type='tabular', framework="keras", algorithm="cnn", model_type="BlackBox", subject_name="subject_name", target_names=[], feature_names=[], feature_descriptions=[], model_category="Classification")
            ).translate("model.h5"),
            SilentKerasModel,
        )
        self.assertIsInstance(
            testObj.with_(
                metadata=ModelMetaData(
                    data_type='tabular', framework="torch", algorithm="cnn", model_type="BlackBox", subject_name="subject_name", target_names=[], feature_names=[], feature_descriptions=[], model_category="Classification")
            ).translate("model.h5"),
            SilentTorchModel,
        )
        self.assertIsInstance(
            testObj.with_(
                metadata=ModelMetaData(
                    data_type='tabular', framework="scikit-learn", algorithm="cnn", model_type="BlackBox", subject_name="subject_name", target_names=[], feature_names=[], feature_descriptions=[], model_category="Classification")
            ).translate("model.h5"),
            SilentScikitLearnModel,
        )
