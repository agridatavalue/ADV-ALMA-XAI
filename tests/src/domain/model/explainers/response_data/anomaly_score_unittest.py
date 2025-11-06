import unittest
import pandas as pd

from src.adv_xai_fulfilment.domain.model.explainers.response_data.anomaly_score import AnomalyScore

class TestAnomalyScore(unittest.TestCase):
    def test_from_data_valid(self):
        data = pd.DataFrame({'feature1': [1, 2], 'feature2': [3, 4]})
        anomaly_score_instance = AnomalyScore.from_data(data)
        
        self.assertIsInstance(anomaly_score_instance, AnomalyScore)

    def test_from_data_invalid(self):
        try:
            AnomalyScore.from_data([1, 2, 3])
        except ValueError as e:
            self.assertEqual(str(e), "Data must be a pandas DataFrame")

    def test_assign_scores_valid(self):
        data = pd.DataFrame({'feature1': [1, 2], 'feature2': [3, 4]})
        scores = [0.1, 0.9]
        anomaly_score_instance = AnomalyScore.from_data(data)
        updated_instance = anomaly_score_instance.assign_scores(scores)

        self.assertTrue('scores' in updated_instance._data.columns)
        self.assertEqual(list(updated_instance._data['scores']), scores)

    def test_assign_scores_invalid_length(self):
        data = pd.DataFrame({'feature1': [1, 2], 'feature2': [3, 4]})
        scores = [0.1]
        anomaly_score_instance = AnomalyScore.from_data(data)
        try:
            anomaly_score_instance.assign_scores(scores)
        except ValueError as e:
            self.assertEqual(str(e), "Length of scores must match number of data points")

    def test_to_dict(self):
        data = pd.DataFrame({'feature1': [1, 2], 'feature2': [3, 4]})
        scores = [0.1, 0.9]
        anomaly_score_instance = AnomalyScore.from_data(data).assign_scores(scores)
        result_dict = anomaly_score_instance.to_dict()
        expected_dict = [
            {'feature1': 1, 'feature2': 3, 'scores': 0.1},
            {'feature1': 2, 'feature2': 4, 'scores': 0.9}
        ]
        
        self.assertTrue(result_dict, expected_dict)