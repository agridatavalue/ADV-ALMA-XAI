from src.adv_xai_fulfilment.domain.model.explainers.explainer import Explainer


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
        return [
            Explainer(
                name=e.get("name", ""),
                type=e.get("type", []),
                categories=e.get("category", []),
                explanations=e.get("explanations", ""),
                is_distributed=e.get("is_distributed", False),
                train_set_required=e.get("train_set_required", False),
                has_categorical_features=e.get("has_categorical_features", False),
                data_type_explainers=e.get("data_type_explainers", []),
            )
            for e in data
        ]
