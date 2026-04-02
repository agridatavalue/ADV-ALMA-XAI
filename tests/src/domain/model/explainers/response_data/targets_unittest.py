import unittest
import numpy as np
import pandas as pd

from src.adv_xai_fulfilment.domain.model.explainers.response_data.targets import Targets

class TargetsTestCase(unittest.TestCase):
    def test_to_dict(self):
        targets = Targets()
        targets.set_x([1, 2, 3])
        targets.set_y([[0, 1, 0]], [0.1, 0.9, 0.2])
        
        expected_dict = {
            'y_real': [0, 1, 0],
            'x_real': [1, 2, 3],
            'y_predicted': [0.1, 0.9, 0.2]
        }
        
        self.assertEqual(targets.to_dict(), expected_dict)
        
        targets = Targets()
        targets.set_x([1, 2, 3])
        targets.set_y(pd.DataFrame([[0, 1, 0]]), np.array([0.1, 0.9, 0.2]))
        
        expected_dict = {
            'y_real': [0, 1, 0],
            'x_real': [1, 2, 3],
            'y_predicted': [0.1, 0.9, 0.2]
        }
        
        self.assertEqual(targets.to_dict(), expected_dict)