import unittest

from src.adv_xai_fulfilment.domain.model.algorithm import Algorithm

class AlgorithmTestCase(unittest.TestCase):
    def test_from_string(self):
        self.assertEqual(Algorithm.from_string("KNN"), Algorithm.KNN)
        self.assertEqual(Algorithm.from_string("knn"), Algorithm.KNN)
        self.assertEqual(Algorithm.from_string("RandomForest"), Algorithm.RANDOM_FOREST)
        self.assertEqual(Algorithm.from_string("randomforest"), Algorithm.RANDOM_FOREST)
        self.assertEqual(Algorithm.from_string("XGBoost"), Algorithm.XGBOOST)
        self.assertEqual(Algorithm.from_string("xgboost"), Algorithm.XGBOOST)
        self.assertEqual(Algorithm.from_string("LightGBM"), Algorithm.LIGHTGBM)
        self.assertEqual(Algorithm.from_string("lightgbm"), Algorithm.LIGHTGBM)
        self.assertEqual(Algorithm.from_string("CatBoost"), Algorithm.CATBOOST)
        self.assertEqual(Algorithm.from_string("catboost"), Algorithm.CATBOOST)
        self.assertEqual(Algorithm.from_string("IsolationForest"), Algorithm.ISOLATION_FOREST)
        self.assertEqual(Algorithm.from_string("isolationforest"), Algorithm.ISOLATION_FOREST
        self.assertEqual(Algorithm.from_string("a new algorithm"), "a new algorithm")
