from .data_type import DataType
from .model_category import ModelCategory
from .explainers.responseData.feature_description import FeatureDescription


class ModelMetaData:
    data_type: DataType
    framework: str
    algorithm: str
    model_type: str
    subject_name: str
    _target_names: list[str]
    feature_names: list[str]
    model_category: ModelCategory
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
        self.data_type = DataType.from_string(data_type)
        self.framework = framework
        self.algorithm = algorithm
        self.model_type = model_type
        self.subject_name = subject_name
        self._target_names = target_names
        self.feature_names = feature_names
        self.model_category = ModelCategory.from_string(model_category)
        self.feature_descriptions = feature_descriptions

    @property
    def is_tabular(self) -> bool:
        return self.data_type == DataType.TABULAR

    @property
    def is_image(self) -> bool:
        return self.data_type == DataType.IMAGE

    @property
    def is_regression(self) -> bool:
        return self.model_category == ModelCategory.REGRESSION

    @property
    def is_classification(self) -> bool:
        return self.model_category == ModelCategory.CLASSIFICATION

    def to_dict(self) -> dict:
        return {
            "data_type": str(self.data_type),
            "framework": self.framework,
            "algorithm": self.algorithm,
            "model_type": self.model_type,
            "targetnames": self._target_names,
            "model_category": str(self.model_category),
            "feature_descriptions": [fd.to_dict() for fd in self.feature_descriptions],
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
