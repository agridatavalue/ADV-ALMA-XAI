from logger import get_logger
from ..model.model import Model
from ..model.algorithm import Algorithm
from ..model.model_metadata import ModelMetaData
from ..model.explainers.explainer import Explainer
from ..model.explainers import all as all_class_explainers
from src.adv_xai_fulfilment.infrastructure.constants import Errors

POSSIBLE_FEATURE_IMPORTANCE_EXPLAINER_NAMES = [
    "TreeSHAPinterventional",
    "TsIsolationForestShap",
    "KernelExplainer",
    "DeepExplainer",
    "KernelSHAP",
]

POSSIBLE_KNN_FEATURE_IMPORTANCE_EXPLAINER_NAMES = [
    "KernelExplainer",
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
        if not isinstance(meta_data, ModelMetaData):
            raise ValueError("meta_data is not ModelMetaData instance")
        
        if not isinstance(selected_model, Model):
            raise ValueError(Errors.MODEL_NOT_MODEL)

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

    def get_for_feature_importance(self, algorithm: str) -> list[Explainer]:
        feature_importance_explainers = [
            e
            for e in self._all_explainers_available
            if e.name in POSSIBLE_FEATURE_IMPORTANCE_EXPLAINER_NAMES
        ]
        
        if Algorithm.from_string(algorithm) == Algorithm.KNN:
            return [
                e 
                for e in feature_importance_explainers 
                if e.name in POSSIBLE_KNN_FEATURE_IMPORTANCE_EXPLAINER_NAMES
            ]
        
        # if Algorithm.from_string(algorithm) == Algorithm.RANDOM_FOREST:
        #     return [
        #         e 
        #         for e in feature_importance_explainers 
        #         if e.name in POSSIBLE_RANDOM_FOREST_FEATURE_IMPORTANCE_EXPLAINER_NAMES
        #     ]
            
        return feature_importance_explainers
