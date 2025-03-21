import unittest


from src.adv_xai_fulfilment.domain.model.partner import Partner
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData
from src.adv_xai_fulfilment.domain.model.questions import Answer, Question, Feedback
from src.adv_xai_fulfilment.domain.model.explainer_metadata import ExplainerMetaData
from src.adv_xai_fulfilment.domain.model.explainers.response_data import (
    FeatureImportance,
)
from src.adv_xai_fulfilment.domain.model.explainers.response_data import (
    ModelPerformanceMetrics,
)


class TestExplainerMetaData(unittest.TestCase):

    def test_get_all_feedback(self):
        meta_data = ExplainerMetaData(
            metrics=ModelPerformanceMetrics().add_metric("metric", 0.0),
            meta_data=ModelMetaData("TABULAR", "f", "a", "m", "s", "CLASSIFICATION"),
            target_name="target",
            possible_explainers=[],
            feature_importance=FeatureImportance("feature"),
        )
        meta_data.add_feedback(
            Feedback(partner=Partner('name'), questions=[], explainer_identifier=None)
        )
        meta_data.add_feedback(
            Feedback(partner=Partner('name'), questions=[], explainer_identifier=None)
        )
        meta_data.add_feedback(
            Feedback(partner=Partner('name1'), questions=[], explainer_identifier=None)
        )

        actual = meta_data.get_all_feedback(filter_by=Partner('name'))

        self.assertIsInstance(actual, list)
        self.assertEqual(len(actual), 2)


    def test_to_dict(self):
        meta_data = ExplainerMetaData(
            metrics=ModelPerformanceMetrics().add_metric("metric", 0.0),
            meta_data=ModelMetaData("TABULAR", "f", "a", "m", "s", "CLASSIFICATION"),
            target_name="target",
            possible_explainers=[],
            feature_importance=FeatureImportance("feature"),
        )
        meta_data.add_feedback(
            Question(
                id="1",
                text="text",
                answers=[Answer.create_radio_answer("text", "value")],
            )
        )

        actual = meta_data.to_dict()

        self.assertIsInstance(actual, dict)
        self.assertTrue("model_metadata" in actual)
        self.assertTrue("explainer_metadata" in actual)
        self.assertTrue("feedback_and_improvements" in actual)
        self.assertTrue("compliance_and_ethical_considerations" in actual)
