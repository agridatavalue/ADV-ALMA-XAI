from alibi.explainers import ALE, PartialDependence, PartialDependenceVariance, PermutationImportance,  AnchorText, AnchorTabular, AnchorImage, CEM, CounterfactualRL, Counterfactual, IntegratedGradients, KernelShap, TreeShap, GradientSimilarity
from explainerdashboard import ClassifierExplainer, ExplainerDashboard,  RegressionExplainer

xai_methods_dict = {
    "ALE": {
        "modeltype": ["BlackBox"],
        "modelcategory": ["Classification", "Regression"],
        "datatype": ["Tabular"],
        "explanations": "global",
        "categorical_features": "No",
        "train_set_required": "No",
        "distributed": "No"
    },
    "RegressionExplainer":{
        "modeltype": ["BlackBox"], #TODO: change it! 
        "modelcategory": ["Regression"],
        "datatype": ["Tabular"],
        "explanations": "global",
        "categorical_features": "No",
        "train_set_required": "No",
        "distributed": "No"
    },
    "PartialDependence": {
        "modeltype": ["BlackBox", "WhiteBox"],
        "modelcategory": ["Classification"],
        "datatype": ["Tabular"],
        "explanations": "global",
        "categorical_features": "Yes",
        "train_set_required": "No",
        "distributed": "No"
    },
    "PDVariance": {
        "modeltype": ["BlackBox", "WhiteBox"],
        "modelcategory": ["Classification"],
        "datatype": ["Tabular"],
        "explanations": "global",
        "categorical_features": "Yes",
        "train_set_required": "No",
        "distributed": "No"
    },
    "PermutationImportance": {
        "modeltype": ["BlackBox"],
        "modelcategory": ["Classification"],
        "datatype": ["Tabular"],
        "explanations": "global",
        "categorical_features": "Yes",
        "train_set_required": "No",
        "distributed": "No"
    },
    "Anchors": {
        "modeltype": ["BlackBox"],
        "modelcategory": ["Classification"],
        "datatype": ["Tabular","Text", "Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "For Tabular",
        "distributed": "No"
    },
    "CEM": {
        "modeltype": ["BlackBox", "WhiteBox"],
        "modelcategory": ["Classification"],
        "datatype": ["Tabular","Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "No",
        "distributed": "No"
    },
    "Counterfactuals": {
        "modeltype": ["BlackBox", "WhiteBox"],
        "modelcategory": ["Classification"],
        "datatype": ["Tabular", "Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "No",
        "distributed": "No"
    },
    "PrototypeCounterfactuals": {
        "modeltype": ["BlackBox", "WhiteBox"],
        "modelcategory": ["Classification"],
        "datatype": ["Tabular", "Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "Optional",
        "distributed": "No"
    },
    "CounterfactualsWithRL": {
        "modeltype": ["BlackBox", "WhiteBox"],
        "modelcategory": ["Classification"],
        "datatype": ["Tabular", "Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "Yes",
        "distributed": "No"
    },
    "IntegratedGradients": {
        "modeltype": ["BlackBox"],
        "modelcategory": ["Classification"],
        "datatype": ["Tabular", "Text", "Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "Optional",
        "distributed": "No"
    },
    "KernelSHAP": {
        "modeltype": ["BlackBox"],
        "modelcategory": ["Classification"],
        "datatype": ["Tabular"],
        "explanations": "both",
        "categorical_features": "Yes",
        "train_set_required": "Yes",
        "distributed": "Yes"
    },
    "TreeSHAP": {
        "modeltype": ["WhiteBox"],
        "modelcategory": ["Classification"],
        "datatype": ["Tabular"],
        "explanations": "both",
        "categorical_features": "Yes",
        "train_set_required": "Optional",
        "distributed": "No"
    },
    "SimilarityExplanations": {
        "modeltype": ["WhiteBox"],
        "modelcategory": ["Classification"],
        "datatype": ["Tabular", "Text", "Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "Yes",
        "distributed": "No"
    }
}


explainer_mapping = {"ALE":{'Tabular':ALE},
                     "RegressionExplainer": {'Tabular':RegressionExplainer},
                        "PartialDependence":{'Tabular':PartialDependence},
                        "PartialDependenceVariance":{'Tabular':PartialDependenceVariance},
                        "PermutationImportance":{'Tabular': PermutationImportance},
                        "Anchors":{'Text':AnchorText, 'Tabular':AnchorTabular, 'Image': AnchorImage},
                        "PertinentPositive": {'Tabular': PermutationImportance, 'Image': PermutationImportance},
                        "Integrated Gradients": {'Text':IntegratedGradients, 'Tabular':IntegratedGradients, 'Image': IntegratedGradients},
                        "KernelSHAP": {'Tabular':KernelShap},
                        "TreeSHAPpathdependent": {'Tabular':TreeShap},
                        "TreeSHAPinterventional": {'Tabular':TreeShap},
                        "CounterfactualInstances": {'Tabular': Counterfactual, 'Image': Counterfactual},
                        "ContrastiveExplanationMethod":{'Tabular':CEM, 'Image':CEM},
                        "CounterfactualsPrototypes":{'Tabular':CounterfactualRL, 'Image':CounterfactualRL},
                        "CounterfactualswithReinforcementLearning": {'Tabular':CounterfactualRL, 'Image':CounterfactualRL},
                        "Similarity explanations": {'Text':GradientSimilarity, 'Tabular':GradientSimilarity, 'Image': GradientSimilarity}
                        }


