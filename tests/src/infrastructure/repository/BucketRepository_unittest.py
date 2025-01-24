import os
import unittest
from unittest.mock import Mock

from src.adv_xai_fulfilment.infrastructure.repository.BucketRepository import \
    BucketRepository


class FakeMinioResponse:
    object_name = "object_name"


class TestBucketRepository(unittest.TestCase):
    def test_download_from(self):
        test_obj = BucketRepository(
            {
                "endpoint": "",
                "access_key": "",
                "secret_key": "",
                "secure": "",
                "region": "",
            }
        )

        with open("object_name", "w") as f:
            f.write("This is a test file.")
        test_obj._client = Mock()
        test_obj._client.fget_object.return_value = FakeMinioResponse()

        self.assertEqual(
            test_obj.download_from("bucket_name", "object_name"), "object_name"
        )
        self.assertEqual(
            test_obj.download_from("bucket_name", "object_name", "destination_file_path"),
            "destination_file_path",
        )
        if os.path.exists("object_name"):
            os.remove("object_name")
        os.remove("destination_file_path")

    def test_upload_to(self):
        test_obj = BucketRepository(
            {
                "endpoint": "",
                "access_key": "",
                "secret_key": "",
                "secure": "",
                "region": "",
            }
        )

        test_obj._client = Mock()
        test_obj._client.fput_object.return_value = type(
            "Result", (), {"object_name": "target_filepath"}
        )()

        self.assertEqual(
            test_obj.upload_to("bucket_name", "target_filepath", "local_filepath"),
            "target_filepath",
        )
