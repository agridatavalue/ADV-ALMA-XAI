import unittest

from src.adv_xai_fulfilment.domain.model.ExplainerMetaData import ExplainerMetaData
from src.adv_xai_fulfilment.domain.model.explainers.AleExplainer import AleExplainer
from src.adv_xai_fulfilment.infrastructure.service.DataLoaderService import (
    DataLoaderService,
)


class TestDataLoaderService(unittest.TestCase):

    def test_upload(self):
        testObj = DataLoaderService()
        testObj._bucketRepository.upload_to = (
            lambda bucket_name, target_filepath, local_filepath: "test/metadata.json"
        )
        dest = testObj.upload(
            explainer_data=ExplainerMetaData({}, [AleExplainer()], {"a": "b"}),
            pilot="test",
        )

        self.assertEqual(dest, "test/metadata.json")
