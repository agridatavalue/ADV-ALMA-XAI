import unittest

from dotenv import load_dotenv

from src.adv_xai_fulfilment.infrastructure.service.data_loader_service import \
    DataLoaderService

load_dotenv()


class TestDataLoaderService(unittest.TestCase):
    def setUp(self):
        self.testObj = DataLoaderService()
