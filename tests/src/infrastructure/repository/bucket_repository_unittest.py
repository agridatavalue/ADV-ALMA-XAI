import os
import unittest
from unittest.mock import Mock

from src.adv_xai_fulfilment.infrastructure.repository import BucketRepository


class FakeMinioResponse:
    object_name: str
    
    def __init__(self, name: str = "object_name"):
        self.object_name = name


class TestBucketRepository(unittest.TestCase):
    def setUp(self):
        self.test_obj = BucketRepository(
            {
                "endpoint": "",
                "access_key": "",
                "secret_key": "",
                "secure": "",
                "region": "",
            }
        )
        
    def test_is_directory_with_directory_path(self):
        self.test_obj._client.list_objects = Mock(return_value=[
            FakeMinioResponse("ai_flows/CNN_InAgro_2025-09-25_23-22-12/test_dataset/X_test.npy")
        ])
        
        self.assertTrue(
            self.test_obj.is_directory("bucket_name", "ai_flows/CNN_InAgro_2025-09-25_23-22-12/test_dataset")
        )
    
    def test_is_directory_with_file_path(self):
        self.test_obj._client.list_objects = Mock(return_value=[])
        
        self.assertFalse(
            self.test_obj.is_directory("bucket_name", "ai_flows/CNN_InAgro_2025-09-25_23-22-12/test_dataset/X_test.npy")
        )
    
    def test_download_from(self):
        with open("object_name", "w") as f:
            f.write("This is a test file.")
        self.test_obj._client = Mock()
        self.test_obj._client.fget_object.return_value = FakeMinioResponse()

        self.assertEqual(
            self.test_obj.download_from("bucket_name", "object_name"), "object_name"
        )
        self.assertEqual(
            self.test_obj.download_from(
                "bucket_name", "object_name", "destination_file_path"
            ),
            "destination_file_path",
        )
        if os.path.exists("object_name"):
            os.remove("object_name")
        os.remove("destination_file_path")

    def test_upload_to(self):
        self.test_obj._client = Mock()
        self.test_obj._client.fput_object.return_value = type(
            "Result", (), {"object_name": "target_filepath"}
        )()

        self.assertEqual(
            self.test_obj.upload_to("bucket_name", "target_filepath", "local_filepath"),
            "target_filepath",
        )
