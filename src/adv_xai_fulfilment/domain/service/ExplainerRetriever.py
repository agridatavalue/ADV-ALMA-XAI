import logging

from ..model.Model import Model
from ..model.ModelMetaData import ModelMetaData
from ..model.explainers.Explainer import Explainer
from ..model.explainers import all as all_class_explainers
from src.adv_xai_fulfilment.infrastructure.Constants import Errors

POSSIBLE_FEATURE_IMPORTANCE_EXPLAINER_NAMES = [
    "KernelExplainer",
    "DeepExplainer",
    "KernelSHAP",
]


class ExplainerRetriever:
    _all_explainers_available: list[Explainer]

    def __init__(self, class_explainers: list[Explainer] = all_class_explainers):
        logging.debug("creating all Explainers")
        self._all_explainers_available = [c() for c in class_explainers]

    def get_by_data(
        self, selected_model: Model, meta_data: ModelMetaData
    ) -> list[Explainer]:
        assert isinstance(
            meta_data, ModelMetaData
        ), "meta_data is not ModelMetaData instance"
        assert isinstance(selected_model, Model), Errors.MODEL_NOT_MODEL

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
