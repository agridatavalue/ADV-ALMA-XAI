import os
import unittest
from unittest.mock import MagicMock, patch

from src.adv_xai_fulfilment.infrastructure.service.data_loader_service import DataLoaderService
from src.adv_xai_fulfilment.domain.model.data_type import DataType
from src.adv_xai_fulfilment.domain.model.explainer_identifier import ExplainerIdentifier
from src.adv_xai_fulfilment.domain.model.model_data import ModelData
from src.adv_xai_fulfilment.domain.model.deep_learning_model_data import DeepLearningModelData

class TestDataLoaderService(unittest.TestCase):
    def setUp(self):
        # Istanza del service
        self.service = DataLoaderService()

        # Mock di ExplainerIdentifier
        self.expl_id = MagicMock(spec=ExplainerIdentifier)
        self.expl_id.data = "predict.csv"
        self.expl_id.data_for_training = "train.csv"
        self.expl_id.get_data_locale_filepath.side_effect = lambda x: f"/tmp/{x}"
        self.expl_id.get_data_for_training_locale_filepath.side_effect = lambda x: f"/tmp/{x}"

        # Imposta attributi necessari per DeepLearningModelData
        self.expl_id._basepath = "/tmp/model"
        self.expl_id.model_filename = "partner_id"

        # Mock repository e file reader
        self.service._file_reader_repository = MagicMock()
        self.service._bucketRepository = MagicMock()

    def test_load_tabular_calls_load_data(self):
        self.service._file_reader_repository.read.return_value = "fake_data"
        self.service._bucketRepository.is_directory.return_value = False

        result = self.service.load(self.expl_id, DataType.TABULAR)

        self.assertIsInstance(result, ModelData)
        self.assertEqual(result.data_predict, "fake_data")
        self.assertEqual(result.data_train, "fake_data")
        # read chiamato sia per predict che train
        self.assertEqual(self.service._file_reader_repository.read.call_count, 2)
        self.service._file_reader_repository.read.assert_any_call('/tmp/predict.csv')
        self.service._file_reader_repository.read.assert_any_call('/tmp/train.csv')

    def test_load_images_returns_list(self):
        self.service._bucketRepository.listdir.return_value = ["img1.png", "img2.png"]
        self.service._bucketRepository.download_from.side_effect = lambda bucket_name, object_name, destination_file_path: destination_file_path

        images = self.service.load_images(self.expl_id)

        self.assertIsInstance(images, list)
        self.assertEqual(len(images), 2)
        self.assertTrue(all(isinstance(i, ModelData) for i in images))
        self.assertTrue(all(hasattr(i, "_image_path") for i in images))

    def test_load_unsupported_data_type_raises(self):
        with self.assertRaises(ValueError):
            self.service.load(self.expl_id, data_type="unsupported")

    def test_load_data_single_file(self):
        self.service._file_reader_repository.read.return_value = "train_content"
        self.service._bucketRepository.is_directory.return_value = False

        data = self.service.load_data(self.expl_id)
        self.assertEqual(data.data_train, "train_content")
        self.assertEqual(data.data_predict, "train_content")

    def test_load_data_folder_files(self):
        self.service._file_reader_repository.read.side_effect = lambda x: f"content_{x}"
        self.service._bucketRepository.listdir.return_value = ["file1.csv", "file2.csv"]
        self.service._bucketRepository.is_directory.return_value = True

        self.expl_id.data_for_training = "train_folder"
        data = self.service.load_data(self.expl_id)

        # Controlla attributi dinamici
        dynamic_attrs = [attr for attr in data.__dict__ if attr.endswith("_train") and attr.startswith("file")]
        print('\n\n>>> 1:',data.__dict__, '2:',dynamic_attrs)
        self.assertTrue(len(dynamic_attrs) == 2)
        for attr in dynamic_attrs:
            self.assertIn("content_", getattr(data, attr))

    def test_load_data_deep_learning_model(self):
        self.service._file_reader_repository.read.return_value = "dl_content"
        self.service._bucketRepository.is_directory.return_value = False

        # Forza algoritmo deep learning
        data = self.service.load_data(self.expl_id, algorithm="tensorflow")
        self.assertIsInstance(data, ModelData)
        self.assertEqual(data.data_train, "dl_content")
        self.assertEqual(data.data_predict, "dl_content")

