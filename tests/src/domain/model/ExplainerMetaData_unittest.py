import unittest


from src.adv_xai_fulfilment.domain.model.questions.Answer import Answer
from src.adv_xai_fulfilment.domain.model.questions.Question import Question
from src.adv_xai_fulfilment.domain.model.ExplainerMetaData import ExplainerMetaData


class TestExplainerMetaData(unittest.TestCase):

    def test_to_dict(self):
        meta_data = ExplainerMetaData(
            metrics={},
            meta_data={},
            target_name="target",
            possible_explainers=[],
            feature_importance={},
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
