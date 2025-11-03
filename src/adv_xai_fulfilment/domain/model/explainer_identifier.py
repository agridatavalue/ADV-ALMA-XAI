import re
import os
from pathlib import Path
from typing import Optional

from .partner import Partner
from .explainers.explainer import Explainer
from ...infrastructure.constants import Errors
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData


BASE_PATH = "ai_flows/"

class ExplainerIdentifier:
    data: str # data for prediction
    data_for_training: str # data for training
    model: str
    partner: Partner

    _metadata: Optional[ModelMetaData]
    metadata_identifier: str

    prediction_target: str

    category: str

    def __init__(
        self,
        *,
        model: str,
        partner: Partner,
        metadata_identifier: str,
        prediction_target: str,
        data: str = "",
        data_for_training: str = "",
    ):
        self.data = data
        self.model = model
        self.partner = partner
        self.category = ""
        self._metadata = None
        self.data_for_training = data_for_training  
        self.prediction_target = prediction_target
        self.metadata_identifier = metadata_identifier

        self._basepath = os.getenv("TEMP", "/tmp")

    @property
    def metadata(self) -> Optional[ModelMetaData]:
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: ModelMetaData):
        if not isinstance(metadata, ModelMetaData):
            raise ValueError(Errors.METADATA_NOT_INSTANCE_OF_MODEL_METADATA)
        
        self._metadata = metadata
        self.category = metadata.model_category

    def _get_base_path(self) -> str:
        model_name = os.path.basename(self.model)
        prediction = self.__sanitize_for_path(self.prediction_target)
        category = self.category.lower()
        partner_id = self.partner.id.replace('/', '')
        return f"{BASE_PATH}{model_name}/{prediction}_{category}/{partner_id}"

    def get_explainer_metadata_path(self) -> str:
        return f"{self._get_base_path()}/metadata.json"

    def get_explainer_data_path(self, filepath: str) -> str:
        return f"{self._get_base_path()}/{self.data}/{os.path.basename(filepath)}"

    def get_explainer_file_path(self, filename: str) -> str:
        base_path = self._get_base_path().replace(BASE_PATH, "explainers/")
        return f"{base_path}/{filename}".lower()
    
    # LOCALE ---------------------------------------------------------------
    def get_feedback_file_locale_path(self) -> str:
        return os.path.join(
            self._basepath, os.path.basename(self.model), "feedback.json"
        )

    def get_model_locale_filepath(self) -> str:
        if self.__check_if_locale_file_exists(self.model):
            return self.model
        
        model_filename: str = os.path.basename(self.model)
        file_extension: str = os.path.splitext(model_filename)[1]
        return os.path.join(self._basepath, model_filename, 'model' + file_extension)

    def get_model_metadata_locale_filepath(self) -> str:
        if self.__check_if_locale_file_exists(self.metadata_identifier):
            return self.metadata_identifier
        
        model_filename: str = os.path.basename(self.model)
        return os.path.join(self._basepath, model_filename, "metadata.json")

    def get_explainer_metadata_locale_filepath(self) -> str:
        model_filename: str = os.path.basename(self.model)
        return os.path.join(
            self._basepath, model_filename, self.partner.id, "metadata.json"
        )

    def get_data_locale_filepath(self, filename: str) -> str:
        if not isinstance(filename, str):
            raise ValueError("filename must be a string")
        
        if self.__check_if_locale_file_exists(filename):
            return filename
        
        model_filename: str = os.path.basename(self.model)
        
        return os.path.join(
            self._basepath, model_filename, self.partner.id, "data", filename if filename != "data" else ""
        )
        
    def get_data_for_training_locale_filepath(self, filename: str) -> str:
        if not isinstance(filename, str):
            raise ValueError("filename must be a string")
        
        if self.__check_if_locale_file_exists(filename):
            return filename
        
        model_filename: str = os.path.basename(self.model)
        
        return os.path.join(
            self._basepath, model_filename, self.partner.id, "data_for_train", filename if filename != "data_train" else ""
        )

    def get_explainer_locale_filepath(self, expl: Explainer) -> str:
        if not isinstance(expl, Explainer):
            raise ValueError("expl must be an instance of Explainer")
    
        model_filename: str = os.path.basename(self.model)
        return os.path.join(
            self._basepath, model_filename, self.partner.id, expl.file_name
        )
    # ------------------------------------------------------------------------

    def __repr__(self) -> str:
        string_to_return = f"ExplainerIdentifier(model={self.model}"
        for attr in ["category", "data", "data_for_training", "metadata_identifier", "prediction_target"]:
            if getattr(self, attr):
                string_to_return += f", {attr}={getattr(self, attr)}"
        return string_to_return + ")"

    def __sanitize_for_path(self, string: str) -> str:
        sanitized_string = re.sub(r"[^a-zA-Z0-9]", "", string)
        return sanitized_string.replace(" ", "_").lower()
    
    def __check_if_locale_file_exists(self, filepath: str) -> bool:
        check_path = Path(filepath).expanduser().resolve()
        return check_path.is_file()
