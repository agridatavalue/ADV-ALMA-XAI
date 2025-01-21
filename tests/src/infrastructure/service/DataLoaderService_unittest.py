import os
import unittest
from os import path
from dotenv import load_dotenv

from src.adv_xai_fulfilment.domain.model.Pilot import Pilot
from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.ExplainerMetaData import ExplainerMetaData
from src.adv_xai_fulfilment.domain.model.explainers.AleExplainer import AleExplainer
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier
from src.adv_xai_fulfilment.infrastructure.service.DataLoaderService import (
    DataLoaderService,
)

load_dotenv()


class TestDataLoaderService(unittest.TestCase):
    def setUp(self):
        self.testObj = DataLoaderService()
