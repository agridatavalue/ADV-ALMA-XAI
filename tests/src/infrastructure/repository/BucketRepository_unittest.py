import unittest

from src.adv_xai_fulfilment.infrastructure.repository.BucketRepository import (
    BucketRepository,
)


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
        test_obj._client = type(
            "Minio",
            (),
            {"fget_object": lambda bucket_name, object_name, file_path: None},
        )

        self.assertEqual(
            test_obj.download_from("bucket_name", "object_name"), "object_name"
        )
        self.assertEqual(
            test_obj.download_from(
                "bucket_name", "object_name", "destination_file_path"
            ),
            "destination_file_path",
        )

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
        test_obj._client = type(
            "Minio",
            (),
            {
                "fput_object": lambda bucket_name, file_path, object_name: type(
                    "Result", (), {"object_name": "target_filepath"}
                )()
            },
        )

        self.assertEqual(
            test_obj.upload_to("bucket_name", "target_filepath", "local_filepath"),
            "target_filepath",
        )
