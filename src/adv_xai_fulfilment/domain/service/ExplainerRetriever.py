import logging

from ..model.Model import Model
from ..model.explainers.Explainer import Explainer
from ..model.explainers import all as all_class_explainers


class ExplainerRetriever:
    _all_explainers_available: list[Explainer]

    def __init__(self, class_explainers: list[Explainer] = all_class_explainers):
        logging.debug("creating all Explainers")
        self._all_explainers_available = [c() for c in class_explainers]

    def get_by_data(self, selected_model: Model, meta_data: dict) -> list[Explainer]:
        assert isinstance(meta_data, dict)
        assert isinstance(selected_model, Model)

        return [
            expl.set_meta_data(meta_data)
            for expl in self._all_explainers_available
            if expl.can_match_with(selected_model, meta_data)
        ]

    def get_by_name(self, name: str) -> Explainer:
        assert isinstance(name, str)
        return next(
            expl for expl in self._all_explainers_available if expl.name == name
        )
