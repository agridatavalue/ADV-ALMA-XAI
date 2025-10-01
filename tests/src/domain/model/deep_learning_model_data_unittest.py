import unittest
import numpy as np

from src.adv_xai_fulfilment.domain.model.deep_learning_model_data import DeepLearningModelData

class TestDeepLearningModelData(unittest.TestCase):
    def test_is_empty_with_none_data(self):
        model_data = DeepLearningModelData()
        model_data.data_predict = None
        model_data.data_train = None
        self.assertTrue(model_data.is_empty)

    def test_is_empty_with_empty_dataframes(self):
        import pandas as pd
        model_data = DeepLearningModelData()
        model_data.data_predict = np.ndarray([])
        model_data.data_train = pd.DataFrame()
        self.assertTrue(model_data.is_empty)

    def test_is_empty_with_non_empty_dataframes(self):
        import pandas as pd
        model_data = DeepLearningModelData()
        model_data.data_predict = np.array([[1, 2], [3, 4]])
        model_data.data_train = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
        self.assertFalse(model_data.is_empty)

