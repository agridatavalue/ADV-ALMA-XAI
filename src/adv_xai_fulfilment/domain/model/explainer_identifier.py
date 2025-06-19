import re
import os

from .partner import Partner
from .explainers.explainer import Explainer
from ...infrastructure.constants import Errors
from src.adv_xai_fulfilment.domain.model.model_metadata import ModelMetaData


class ExplainerIdentifier:
    data: str
    model: str
    partner: Partner

    _metadata: ModelMetaData
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
    ):
        self.data = data
        self.model = model
        self.partner = partner
        self.category = ""
        self._metadata = None
        self.prediction_target = prediction_target
        self.metadata_identifier = metadata_identifier

        self._basepath = os.getenv("TEMP", "/tmp")

    @property
    def metadata(self) -> ModelMetaData:
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: ModelMetaData):
        assert isinstance(
            metadata, ModelMetaData
        ), Errors.METADATA_NOT_INSTANCE_OF_MODEL_METADATA
        self._metadata = metadata
        self.category = metadata.model_category

    def _get_base_path(self) -> str:
        return f"{os.path.basename(self.model)}/{self.__sanitize_for_path(self.prediction_target)}_{self.category.lower()}/{self.partner.id.replace('/', '')}"

    def get_explainer_metadata_path(self) -> str:
        return f"{self._get_base_path()}/metadata.json"

    def get_explainer_data_path(self, filepath: str) -> str:
        return f"{self._get_base_path()}/{self.data}/{os.path.basename(filepath)}"

    def get_explainer_file_path(self, filename: str) -> str:
        return f"{self._get_base_path()}/{filename}".lower()
    
    # LOCALE ---------------------------------------------------------------
    def get_feedback_file_locale_path(self) -> str:
        return os.path.join(
            self._basepath, os.path.basename(self.model), "feedback.json"
        )

    def get_model_locale_filepath(self) -> str:
        model_filename: str = os.path.basename(self.model)
        file_extension: str = os.path.splitext(model_filename)[1]
        return os.path.join(self._basepath, model_filename, 'model' + file_extension)

    def get_model_metadata_locale_filepath(self) -> str:
        model_filename: str = os.path.basename(self.model)
        return os.path.join(self._basepath, model_filename, "metadata.json")

    def get_explainer_metadata_locale_filepath(self) -> str:
        model_filename: str = os.path.basename(self.model)
        return os.path.join(
            self._basepath, model_filename, self.partner.id, "metadata.json"
        )

    def get_data_locale_filepath(self, filename: str) -> str:
        assert isinstance(filename, str), "filename must be a string"
        model_filename: str = os.path.basename(self.model)
        return os.path.join(
            self._basepath, model_filename, self.partner.id, "data", filename
        )

    def get_explainer_locale_filepath(self, expl: Explainer) -> str:
        assert isinstance(expl, Explainer), "expl must be an instance of Explainer"
        model_filename: str = os.path.basename(self.model)
        return os.path.join(
            self._basepath, model_filename, self.partner.id, expl.file_name
        )
    # ------------------------------------------------------------------------

    def __repr__(self) -> str:
        string_to_return = f"ExplainerIdentifier(model={self.model}"
        for attr in ["category", "data", "metadata_identifier", "prediction_target"]:
            if getattr(self, attr):
                string_to_return += f", {attr}={getattr(self, attr)}"
        return string_to_return + ")"

    def __sanitize_for_path(self, string: str) -> str:
        sanitized_string = re.sub(r"[^a-zA-Z0-9]", "", string)
        return sanitized_string.replace(" ", "_").lower()
