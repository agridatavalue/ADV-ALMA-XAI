import unittest
from unittest.mock import MagicMock

from src.adv_xai_fulfilment.domain.model.models.Model import Model
from src.adv_xai_fulfilment.infrastructure.service.ModelLoaderService import (
    ModelLoaderService,
)
from src.adv_xai_fulfilment.infrastructure.repository.PersistenceRepository import (
    PersistenceRepository,
)


class ModelLoaderServiceTest(unittest.TestCase):
    testObj: ModelLoaderService

    def setUp(self):
        self.testObj = ModelLoaderService()

    def test_createFromDict_negative(self):
        persistenceRepository = PersistenceRepository()
        persistenceRepository.read = MagicMock(
            return_value={
                "models": [
                    {
                        "name": "ALE",
                        "modeltype": ["BlackBox"],
                        "modelcategory": ["Classification", "Regression"],
                        "datatype": ["Tabular"],
                        "explanations": "global",
                        "categorical_features": "No",
                        "train_set_required": "No",
                        "distributed": "No",
                    }
                ]
            }
        )
        self.testObj._persistenceRepository = persistenceRepository
        actual = self.testObj.loadFrom("test.json")

        self.assertTrue(isinstance(actual, list))
        self.assertEqual(len(actual), 1)
        self.assertTrue(isinstance(actual[0], Model))


if __name__ == "__main__":
    unittest.main()
