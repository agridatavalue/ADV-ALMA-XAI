import unittest


from src.adv_xai_fulfilment.presentation.validator.explainer_generator_validator import ExplainerGeneratorValidator

class TestExplainerGeneratorValidator(unittest.TestCase):
    def test_validate_and_sanitize_build_valid(self):
        validator = ExplainerGeneratorValidator()
        data = {
            "model": "test_model",
            "partner": "test_partner",
            "data_for_train": "/path/to/train/data.csv",
            "data_for_predict": "https://minio.store.platform.agridatavalue.eu/agridatavalue/ai_flows/yyy_test_retrain_model_274cb650-713e-4c07-994d-67b74b340cf9/datasets/Retrain_2025-08-28_13-21-34/data.csv"
        }
        sanitized_data = validator.validate_and_sanitize_build(data)
        self.assertEqual(sanitized_data["data_for_train"], "/path/to/train/data.csv")
        self.assertEqual(sanitized_data["data_for_predict"], "ai_flows/yyy_test_retrain_model_274cb650-713e-4c07-994d-67b74b340cf9/datasets/Retrain_2025-08-28_13-21-34/data.csv")
        
    def test_validate_and_sanitize_build_for_last_slash_in_paths(self):
        validator = ExplainerGeneratorValidator()
        data = {
            "model": "test_model",
            "partner": "test_partner",
            "data_for_train": "/path/to/train",
            "data_for_predict": "https://minio.store.platform.agridatavalue.eu/agridatavalue/ai_flows/yyy_test_retrain_model_274cb650-713e-4c07-994d-67b74b340cf9/datasets/Retrain_2025-08-28_13-21-34/"
        }
        sanitized_data = validator.validate_and_sanitize_build(data)
        self.assertEqual(sanitized_data["data_for_train"], "/path/to/train")
        self.assertEqual(sanitized_data["data_for_predict"], "ai_flows/yyy_test_retrain_model_274cb650-713e-4c07-994d-67b74b340cf9/datasets/Retrain_2025-08-28_13-21-34")