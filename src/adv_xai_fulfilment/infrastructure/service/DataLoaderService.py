import os
import json
import logging
import pandas as pd

from ..Helper import Helper
from ...domain.model.ModelMetaData import ModelMetaData
from ..repository.BucketRepository import BucketRepository
from ...domain.model.ExplainerMetaData import ExplainerMetaData
from src.adv_xai_fulfilment.infrastructure.Constants import Errors
from .translator.ModelMetaDataTranslator import ModelMetaDataTranslator
from .translator.ExplainerMetaDataTranslator import ExplainerMetaDataTranslator
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier


class DataLoaderService:
    _translator: ModelMetaDataTranslator
    _bucketRepository: BucketRepository
    _model_metadata_translator: ModelMetaDataTranslator
    _explainer_metadata_translator: ExplainerMetaDataTranslator

    def __init__(self):
        self._bucketRepository = BucketRepository(
            {
                "endpoint": os.getenv("MINIO_ENDPOINT"),
                "access_key": os.getenv("MINIO_ACCESS_KEY"),
                "secret_key": os.getenv("MINIO_SECRET_KEY"),
                "secure": os.getenv("MINIO_SECURE", "true").lower() == "true",
            }
        )
        self._model_metadata_translator = ModelMetaDataTranslator()
        self._explainer_metadata_translator = ExplainerMetaDataTranslator()

    def load_data(self, folder_path: str, bucket_name: str) -> dict[str, pd.DataFrame]:
        if not folder_path:
            return None

        x_file_path: str = folder_path + "/x.csv"
        y_file_path: str = folder_path + "/y.csv"

        if not Helper.is_local_path(x_file_path):
            logging.debug(
                f"is not a local path, downloading {x_file_path} from {bucket_name}"
            )
            file_x: str = self._bucketRepository.download_from(
                bucket_name=bucket_name,
                object_name=x_file_path,
                destination_file_path="x.csv",
            )

        if not Helper.is_local_path(y_file_path):
            logging.debug(
                f"is not a local path, downloading {y_file_path} from {bucket_name}"
            )
            file_y: str = self._bucketRepository.download_from(
                bucket_name=bucket_name,
                object_name=y_file_path,
                destination_file_path="y.csv",
            )

        data = {"x": pd.read_csv(file_x), "y": pd.read_csv(file_y)}
        os.remove(file_x)
        os.remove(file_y)

        return data

    def load_file(self, file_path: str, bucket_name: str) -> pd.DataFrame:
        file: str = self._bucketRepository.download_from(
            object_name=file_path,
            bucket_name=bucket_name,
        )
        return pd.read_csv(file)

    def load_explainer_metadata(
        self, expl_id: ExplainerIdentifier
    ) -> ExplainerMetaData:
        assert isinstance(
            expl_id, ExplainerIdentifier
        ), Errors.EXPLAINER_IDENTIFIER_NOT_EXPLAINER_IDENTIFIER

        file: str = self._bucketRepository.download_from(
            object_name=expl_id.get_metadata_path(),
            bucket_name=os.getenv("EXPLAINER_FOLDER_PATH"),
        )
        with open(file, "r") as json_file:
            metadata = json.load(json_file) or {}

        os.remove(file)
        return self._explainer_metadata_translator.translate(metadata)

    def load_model_metadata(
        self, explainer_identifier: ExplainerIdentifier
    ) -> ModelMetaData:
        assert isinstance(
            explainer_identifier, ExplainerIdentifier
        ), Errors.EXPLAINER_IDENTIFIER_NOT_EXPLAINER_IDENTIFIER

        file: str = self._bucketRepository.download_from(
            object_name=explainer_identifier.metadata.lower(),
            bucket_name=os.getenv("MODEL_FOLDER_PATH"),
        )
        with open(file, "r") as json_file:
            metadata = json.load(json_file) or {}

        os.remove(file)
        return self._model_metadata_translator.translate(metadata)

    def upload(
        self,
        explainer_data: ExplainerMetaData,
        target: str,
        model_category: str,
        model_filename: str,
    ) -> str:
        assert isinstance(
            explainer_data, ExplainerMetaData
        ), Errors.EXPLAINER_DATA_NOT_EXPLAINER_METADATA

        if isinstance(explainer_data, ExplainerMetaData):
            filename: str = "metadata.json"
            model_path: str = os.getenv("EXPLAINER_FOLDER_PATH")

        temp_path: str = os.path.join(os.getenv("TEMP"), filename)
        with open(temp_path, "w") as file:
            file.write(json.dumps(explainer_data.to_dict()))

        res: str = self._bucketRepository.upload_to(
            bucket_name=model_path,
            local_filepath=temp_path,
            target_filepath=self.__calculate_explainer_path(
                target, model_category, filename, model_filename
            ),
        )
        os.remove(temp_path)
        return res

    def __calculate_explainer_path(
        self, target: str, model_category: str, filename: str, model_filename: str
    ):
        path: str = os.path.join(model_filename, f"{target}_{model_category}", filename)
        return path.lower().replace(" ", "_").replace("-", "_")
