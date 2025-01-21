import unittest

from src.adv_xai_fulfilment.domain.model.Pilot import Pilot
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers.Explainer import Explainer
from src.adv_xai_fulfilment.domain.model.ExplainerMetaData import ExplainerMetaData
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier
from src.adv_xai_fulfilment.infrastructure.service.ExplainerRepositoryService import (
    ExplainerRepositoryService,
)


class TestExplainerRepositoryService(unittest.TestCase):
    def test_upload_metadata(self):
        test_obj = ExplainerRepositoryService()
        test_obj._bucketRepository.upload_to = lambda *args, **kwargs: "path"

        self.assertEqual(
            test_obj.upload_metadata(
                expl_id=ExplainerIdentifier(
                    model="model",
                    pilot=Pilot("pilot_id"),
                    prediction_target="regression",
                    metadata_identifier="metadata",
                ),
                metadata=ExplainerMetaData(
                    metrics={"metric": "value"},
                    meta_data=ModelMetaData(
                        data_type="",
                        framework="",
                        algorithm="",
                        model_type="",
                        subject_name="",
                        model_category="",
                    ),
                    target_name="",
                    possible_explainers=[
                        Explainer("name", [], [], "category", True, True, True, [])
                    ],
                ),
            ),
            "path",
        )
