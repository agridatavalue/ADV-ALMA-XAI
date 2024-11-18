from .FeatureDescription import FeatureDescription


class ModelMetaData:
    data_type: str
    framework: str
    algorithm: str
    _targetnames: list[str]
    model_category: str
    feature_descriptions: list[FeatureDescription]

    def __init__(
        self,
        data_type: str,
        framework: str,
        algorithm: str,
        model_category: str,
        targetnames: list[str],
        feature_descriptions: list[FeatureDescription],
    ):
        self.data_type = data_type
        self.framework = framework
        self.algorithm = algorithm
        self._targetnames = targetnames
        self.model_category = model_category
        self.feature_descriptions = feature_descriptions

    @property
    def target_names(self) -> list[str]:
        return self._targetnames or []

    def index_of_target_name(self, target_name: str) -> int:
        return (
            self._targetnames.index(target_name)
            if target_name in self._targetnames
            else -1
        )

    @property
    def first_target_name(self) -> str:
        return self._targetnames[0] if self._targetnames else None
