import unittest
from os.path import abspath
from unittest.mock import patch

from src.adv_xai_fulfilment.infrastructure.Helper import Helper


class TestHelper(unittest.TestCase):
    def test_is_local_with_local_file(self):
        self.assertTrue(Helper.is_local(abspath("README.md")))

    def test_is_local_with_remote_file(self):
        url = "http://example.com/remote_file.txt"
        self.assertFalse(Helper.is_local(url))

    def test_is_local_with_nonexistent_file(self):
        url = "file:///path/to/nonexistent_file.txt"
        with patch("os.path.exists", return_value=False):
            self.assertFalse(Helper.is_local(url))

    def test_is_local_with_invalid_url(self):
        self.assertFalse(Helper.is_local("not_a_valid_url"))


if __name__ == "__main__":
    unittest.main()
