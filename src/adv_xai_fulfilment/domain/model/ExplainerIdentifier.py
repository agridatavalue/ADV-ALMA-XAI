import os

from .Pilot import Pilot
from .ModelData import ModelData
from .ModelMetaData import ModelMetaData
from .explainers.Explainer import Explainer
from ...infrastructure.Constants import Errors


class ExplainerIdentifier:
    data: str
    model: str
    pilot: Pilot

    _metadata: ModelMetaData
    metadata_identifier: str

    prediction_target: str

    category: str

    def __init__(
        self,
        *,
        model: str,
        pilot: Pilot,
        metadata_identifier: str,
        prediction_target: str,
        data: str = "",
    ):
        self.data = data
        self.model = model
        self.pilot = pilot
        self.category = ""
        self._metadata = None
        self.prediction_target = prediction_target
        self.metadata_identifier = metadata_identifier

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

    def get_explainer_metadata_path(self) -> str:
        return f"{self.model}/{self.prediction_target.lower()}_{self.category.lower()}/metadata.json"

    def get_model_metadata_locale_filepath(self) -> str:
        return os.path.join(os.getenv("TEMP"), self.model, "metadata.json")

    def get_explainer_metadata_locale_filepath(self) -> str:
        return os.path.join(
            os.getenv("TEMP"), self.model, self.pilot.id, "metadata.json"
        )

    def get_data_locale_filepath(self, filename: str) -> str:
        assert isinstance(filename, str), "filename must be a string"
        return os.path.join(os.getenv("TEMP"), self.model, "data", filename)

    def get_explainer_locale_filepath(self, expl: Explainer) -> str:
        assert isinstance(expl, Explainer), "expl must be an instance of Explainer"
        return os.path.join(
            os.getenv("TEMP"), self.model, self.pilot.id, expl.file_name
        )

    def get_filename_path(self, filename: str) -> str:
        return (
            f"{self.model}/{self.prediction_target}_{self.category}/{filename}".lower()
        )

    def __repr__(self) -> str:
        string_to_return = f"ExplainerIdentifier(model={self.model}"
        for attr in ["category", "data", "metadata_identifier", "prediction_target"]:
            if getattr(self, attr):
                string_to_return += f", {attr}={getattr(self, attr)}"
        return string_to_return + ")"
