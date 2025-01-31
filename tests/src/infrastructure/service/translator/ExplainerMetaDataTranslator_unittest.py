import unittest

from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.ExplainerMetaData import ExplainerMetaData
from src.adv_xai_fulfilment.domain.model.explainers.responseData.FeatureImportance import (
    FeatureImportance,
)
from src.adv_xai_fulfilment.infrastructure.service.translator.ExplainerMetaDataTranslator import (
    ExplainerMetaDataTranslator,
)


class TestExplainerMetaDataTranslator(unittest.TestCase):
    def setUp(self):
        self.testObj = ExplainerMetaDataTranslator()

    def test_translate(self):
        result = self.testObj.translate(
            {
                "model_metadata": {
                    "subjectname": "Leek",
                    "targetname": "Biomass",
                    "modelcategory": "Regression",
                    "explaineed_model_name": "neuralnetwork",
                    "framework": ["Tensorflow", "pytorch", "scikit"],
                    "training_data_summary": "set with 100,000 instances and 20 features and 3 targets",
                    "hyperparameters": {
                        "n_neurons": 100,
                        "activation_fun": "Relu",
                        "n_parameters": 100,
                    },
                    "performance_metrics": {
                        "Mean Squared Error (MSE)": 2304.80129851625,
                        "R-Squared (R\u00b2)": -8.093974859538378,
                        "Mean Absolute Error (MAE)": 45.809314530363324,
                        "Root Mean Squared Error (RMSE)": 48.008346133940606,
                        "Mean Absolute Percentage Error (MAPE)": 1.9062117061080628,
                    },
                },
                "explainer_metadata": {
                    "explainers_identified": ["ALE", "KernelExplainer"],
                    "explanation_method": ["Feature importance", "Model performance"],
                    "scope_of_explanation": ["Local", "Global"],
                    "vizualization type": ["barplot", "scaterplot"],
                },
                "compliance_and_ethical_considerations": {
                    "Rights_for_explanation": "XAI framwork caters to explain and respect the rights of individuals, coopratives and stakholders as outlined in GDPR including rights for explanation",
                    "bias_and_fairness": "No significant biases detected during fairness assessment",
                    "Lawful_bases_of_data_processing": "",
                    "Data_security": "",
                    "regulatory_compliance": "Compliant with GDPR and local regulations",
                },
                "feedback_and_improvements": {},
            }
        )

        self.assertIsInstance(result, ExplainerMetaData)
        self.assertIsInstance(result.model_metadata, ModelMetaData)
        self.assertIsInstance(result.feature_importance, FeatureImportance)
