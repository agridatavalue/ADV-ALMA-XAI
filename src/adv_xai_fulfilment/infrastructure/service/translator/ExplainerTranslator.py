from src.adv_xai_fulfilment.domain.model.explainers.Explainer import Explainer


class ExplainerTranslator:
    def translate(self, data: list[dict]) -> list[Explainer]:
        """
        name: str,
        type: list[str],
        category: list[str],
        explanations: str,
        is_distributed: bool,
        train_set_required: bool,
        has_categorical_features: bool,
        data_type_explainers: list[DataTypeModelExplainer],
        """
        return [Explainer(name=e.get("name", "")) for e in data]
