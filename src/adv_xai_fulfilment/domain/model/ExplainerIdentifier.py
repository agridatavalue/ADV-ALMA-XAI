from .Pilot import Pilot
from .ModelMetaData import ModelMetaData
from ...infrastructure.Constants import Errors


class ExplainerIdentifier:
    data: str
    model: str
    pilot: Pilot
    _metadata: ModelMetaData
    prediction_target: str

    category: str

    def __init__(
        self,
        model: str,
        pilot: Pilot,
        prediction_target: str,
        data: str = "",
        metadata: ModelMetaData = None,
    ):
        self.data = data
        self.model = model
        self.pilot = pilot
        self.category = ""
        self._metadata = metadata
        self.prediction_target = prediction_target

    @property
    def metadata(self) -> ModelMetaData:
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: ModelMetaData):
        assert isinstance(
            metadata, ModelMetaData
        ), Errors.METADATA_NOT_INSTANCE_OF_MODEL_METADATA
        self._metadata = metadata

    def get_metadata_path(self) -> str:
        return f"{self.model}/{self.prediction_target}_{self.category}/metadata.json".lower()

    def get_metadata_locale_filepath(self) -> str:
        return (
            self._metadata.get_local_file_path(
                model=self.model,
                category=self.category,
                prediction_target=self.prediction_target,
            )
            if self._metadata
            else ""
        )

    def get_data_locale_filepath(self) -> str:
        return ModelMetaData.get_local_file_path(
            self.model,
            self.category,
            self.prediction_target,
            self.pilot.id if self.pilot else "",
        )

    def get_filename_path(self, filename: str) -> str:
        return (
            f"{self.model}/{self.prediction_target}_{self.category}/{filename}".lower()
        )

    def __repr__(self) -> str:
        string_to_return = f"ExplainerIdentifier(model={self.model}"
        for attr in ["category", "data", "metadata", "prediction_target"]:
            if getattr(self, attr):
                string_to_return += f", {attr}={getattr(self, attr)}"
        return string_to_return + ")"
