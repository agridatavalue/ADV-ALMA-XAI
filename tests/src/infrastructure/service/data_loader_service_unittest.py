import unittest

from dotenv import load_dotenv

from src.adv_xai_fulfilment.infrastructure.service.DataLoaderService import \
    DataLoaderService

load_dotenv()


class TestDataLoaderService(unittest.TestCase):
    def setUp(self):
        self.testObj = DataLoaderService()
