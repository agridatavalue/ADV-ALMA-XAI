from alibi.explainers import (
    ALE,
    PartialDependence,
    PartialDependenceVariance,
    PermutationImportance,
    AnchorText,
    AnchorTabular,
    AnchorImage,
    CEM,
    CounterfactualRL,
    Counterfactual,
    IntegratedGradients,
    KernelShap,
    TreeShap,
    GradientSimilarity,
)
from explainerdashboard import (
    ClassifierExplainer,
    ExplainerDashboard,
    RegressionExplainer,
)

from .models.Model import Model

explainer_mapping = {
    "ALE": {"Tabular": ALE},
    "RegressionExplainer": {"Tabular": RegressionExplainer},
    "PartialDependence": {"Tabular": PartialDependence},
    "PartialDependenceVariance": {"Tabular": PartialDependenceVariance},
    "PermutationImportance": {"Tabular": PermutationImportance},
    "Anchors": {"Text": AnchorText, "Tabular": AnchorTabular, "Image": AnchorImage},
    "PertinentPositive": {
        "Tabular": PermutationImportance,
        "Image": PermutationImportance,
    },
    "Integrated Gradients": {
        "Text": IntegratedGradients,
        "Tabular": IntegratedGradients,
        "Image": IntegratedGradients,
    },
    "KernelSHAP": {"Tabular": KernelShap},
    "TreeSHAPpathdependent": {"Tabular": TreeShap},
    "TreeSHAPinterventional": {"Tabular": TreeShap},
    "CounterfactualInstances": {"Tabular": Counterfactual, "Image": Counterfactual},
    "ContrastiveExplanationMethod": {"Tabular": CEM, "Image": CEM},
    "CounterfactualsPrototypes": {
        "Tabular": CounterfactualRL,
        "Image": CounterfactualRL,
    },
    "CounterfactualswithReinforcementLearning": {
        "Tabular": CounterfactualRL,
        "Image": CounterfactualRL,
    },
    "Similarity explanations": {
        "Text": GradientSimilarity,
        "Tabular": GradientSimilarity,
        "Image": GradientSimilarity,
    },
}


class Explainer:
    data: dict
    model: Model
    meta_data: dict

    def __init__(self, model: Model, data: dict, meta_data: dict):
        self.data = data
        self.model = model
        self.meta_data = meta_data

    def build_and_save_on_persistence(self, destination_path: str):
        print(
            ">>>",
            explainer_mapping.get(self.model.name).get(self.meta_data.get("datatype")),
        )
