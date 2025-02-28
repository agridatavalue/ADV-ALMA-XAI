import unittest

from src.adv_xai_fulfilment.domain.model.explainers.response_data.heatmap import Heatmap


class TestHeatmap(unittest.TestCase):

    def test_add(self):
        heatmap = Heatmap()
        heatmap.add("path/to/heatmap")
        self.assertEqual(heatmap.heatmaps, ["path/to/heatmap"])

        heatmap.add("path/to/heatmap2").add("path/to/heatmap3").add("path/to/heatmap4")
        self.assertEqual(len(heatmap.heatmaps), 4)

    def test_is_empty(self):
        heatmap = Heatmap()
        self.assertTrue(heatmap.is_empty)

        heatmap.add("path/to/heatmap")
        self.assertFalse(heatmap.is_empty)
