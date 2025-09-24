from typing import Optional

from .data_type import DataType
from .model_category import ModelCategory
from .model_metadata_layer import ModelMetaDataLayer
from .explainers.response_data import FeatureDescription


class ModelMetaData:
    data_type: DataType
    framework: str
    algorithm: str
    n_classes: Optional[int]
    model_type: str
    input_shape: list[int]
    subject_name: str
    _is_federated: bool
    _target_names: list[str]
    feature_names: list[str]
    model_category: ModelCategory
    _architectures: list[ModelMetaDataLayer]
    feature_descriptions: list[FeatureDescription]

    def __init__(
        self,
        data_type: str,
        framework: str,
        algorithm: str,
        model_type: str,
        subject_name: str,
        model_category: str,
        n_classes: Optional[int] = None,
        input_shape: list[int] = [],
        target_names: list[str] = [],
        is_federated: bool = False,
        feature_names: list[str] = [],
        architectures: list[ModelMetaDataLayer] = [],
        feature_descriptions: list[FeatureDescription] = [],
    ):
        self.n_classes = n_classes if isinstance(n_classes, int) else None
        self.data_type = DataType.from_string(data_type)
        self.framework = framework
        self.algorithm = algorithm
        self.model_type = model_type
        self.input_shape = input_shape if isinstance(input_shape, list) else []
        self.subject_name = subject_name
        self._is_federated = is_federated or False
        self._target_names = target_names
        self.feature_names = feature_names
        self._architectures = architectures
        self.model_category = ModelCategory.from_string(model_category)
        self.feature_descriptions = feature_descriptions
    
    @property
    def is_federated(self) -> bool:
        return self._is_federated if self._is_federated is not None else False
    
    @property
    def is_deep_learning(self) -> bool:
        deep_learning_algorithms = ['cnn', 'rnn', 'lstm', 'transformer', 'yolov8']
        return self.algorithm.lower() in deep_learning_algorithms

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
    
    @property
    def architectures(self) -> list[ModelMetaDataLayer]:
        return self._architectures or []
    
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
        return self._target_names[0] if self._target_names else ''

    def __repr__(self) -> str:
        return f"ModelMetaData({self.to_dict})"
