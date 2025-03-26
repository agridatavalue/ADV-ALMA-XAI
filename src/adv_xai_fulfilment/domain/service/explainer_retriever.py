from logger import get_logger
from ..model.model import Model
from ..model.model_metadata import ModelMetaData
from ..model.explainers.explainer import Explainer
from ..model.explainers import all as all_class_explainers
from src.adv_xai_fulfilment.infrastructure.constants import Errors

POSSIBLE_FEATURE_IMPORTANCE_EXPLAINER_NAMES = [
    "TreeSHAPinterventional",
    "KernelExplainer",
    "DeepExplainer",
    "KernelSHAP",
]

logger = get_logger()

class ExplainerRetriever:
    _all_explainers_available: list[Explainer]

    def __init__(self, class_explainers: list[Explainer] = all_class_explainers):
        logger.debug("creating all Explainers")
        self._all_explainers_available = [c() for c in class_explainers]

    def get_by_data(
        self, selected_model: Model, meta_data: ModelMetaData
    ) -> list[Explainer]:
        assert isinstance(
            meta_data, ModelMetaData
        ), "meta_data is not ModelMetaData instance"
        assert isinstance(selected_model, Model), Errors.MODEL_NOT_MODEL

        logger.debug(
            "searching for explainer for this metadata: "
            f"model_type: {meta_data.model_type}, "
            f"model_category: {meta_data.model_category}, "
            f"data_type: {meta_data.data_type}"
        )

        return [
            expl.set_meta_data(meta_data)
            for expl in self._all_explainers_available
            if expl.can_match_with(selected_model, meta_data)
        ]

    def get_by_name(self, name: str) -> Explainer:
        assert isinstance(name, str), Errors.EXPLAINER_NAME_NOT_STRING
        return next(
            expl for expl in self._all_explainers_available if expl.name == name
        )

    def get_for_feature_importance(self) -> list[Explainer]:
        return [
            e
            for e in self._all_explainers_available
            if e.name in POSSIBLE_FEATURE_IMPORTANCE_EXPLAINER_NAMES
        ]
