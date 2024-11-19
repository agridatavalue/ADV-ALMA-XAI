from .DataType import DataType
from .FeatureDescription import FeatureDescription


class ModelMetaData:
    data_type: DataType
    framework: str
    algorithm: str
    model_type: str
    subject_name: str
    _target_names: list[str]
    feature_names: list[str]
    model_category: str
    feature_descriptions: list[FeatureDescription]

    def __init__(
        self,
        data_type: str,
        framework: str,
        algorithm: str,
        model_type: str,
        subject_name: str,
        model_category: str,
        target_names: list[str] = [],
        feature_names: list[str] = [],
        feature_descriptions: list[FeatureDescription] = [],
    ):
        self.data_type = data_type
        self.framework = framework
        self.algorithm = algorithm
        self.model_type = model_type
        self.subject_name = subject_name
        self._target_names = target_names
        self.feature_names = feature_names
        self.model_category = model_category
        self.feature_descriptions = feature_descriptions

    @property
    def to_dict(self) -> dict:
        return {
            "data_type": self.data_type,
            "framework": self.framework,
            "algorithm": self.algorithm,
            "model_type": self.model_type,
            "model_category": self.model_category,
            "targetnames": self._target_names,
            "feature_descriptions": [
                feature_description.to_dict()
                for feature_description in self.feature_descriptions
            ],
        }

    @property
    def target_names(self) -> list[str]:
        return self._target_names or []

    def index_of_target_name(self, target_name: str) -> int:
        return (
            self._target_names.index(target_name)
            if target_name in self._target_names
            else -1
        )

    @property
    def first_target_name(self) -> str:
        return self._target_names[0] if self._target_names else None

    def __repr__(self) -> str:
        return f"ModelMetaData({self.to_dict})"
