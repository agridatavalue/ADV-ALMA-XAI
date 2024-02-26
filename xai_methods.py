xai_methods_dict = {
    "ALE": {
        "modeltype": "BlackBox",
        "modelcategory": "Classification",
        "datatype": ["Tabular"],
        "explanations": "global",
        "categorical_features": "No",
        "train_set_required": "No",
        "distributed": "No"
    },
    "PartialDependence": {
        "modeltype": "BlackBoxWhiteBox",
        "modelcategory": "Classification",
        "datatype": ["Tabular"],
        "explanations": "global",
        "categorical_features": "Yes",
        "train_set_required": "No",
        "distributed": "No"
    },
    "PDVariance": {
        "modeltype": "BlackBoxWhiteBox",
        "modelcategory": "Classification",
        "datatype": ["Tabular"],
        "explanations": "global",
        "categorical_features": "Yes",
        "train_set_required": "No",
        "distributed": "No"
    },
    "PermutationImportance": {
        "modeltype": "BlackBox",
        "modelcategory": "Classification",
        "datatype": "Tabular",
        "explanations": "global",
        "categorical_features": "Yes",
        "train_set_required": "No",
        "distributed": "No"
    },
    "Anchors": {
        "modeltype": "BlackBox",
        "modelcategory": "Classification",
        "datatype": ["Tabular","Text", "Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "For Tabular",
        "distributed": "No"
    },
    "CEM": {
        "modeltype": "BlackBoxWhiteBox",
        "modelcategory": "Classification",
        "datatype": ["Tabular","Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "No",
        "distributed": "No"
    },
    "Counterfactuals": {
        "modeltype": "BlackBoxWhiteBox",
        "modelcategory": "Classification",
        "datatype": ["Tabular", "Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "No",
        "distributed": "No"
    },
    "PrototypeCounterfactuals": {
        "modeltype": "BlackBoxWhiteBox",
        "modelcategory": "Classification",
        "datatype": ["Tabular", "Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "Optional",
        "distributed": "No"
    },
    "CounterfactualsWithRL": {
        "modeltype": "BlackBox",
        "modelcategory": "Classification",
        "datatype": ["Tabular", "Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "Yes",
        "distributed": "No"
    },
    "IntegratedGradients": {
        "modeltype": "BlackBox",
        "modelcategory": "Classification",
        "datatype": ["Tabular", "Text", "Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "Optional",
        "distributed": "No"
    },
    "KernelSHAP": {
        "modeltype": "BlackBox",
        "modelcategory": "Classification",
        "datatype": "Tabular",
        "explanations": "both",
        "categorical_features": "Yes",
        "train_set_required": "Yes",
        "distributed": "Yes"
    },
    "TreeSHAP": {
        "modeltype": "WhiteBox",
        "modelcategory": "Classification",
        "datatype": "Tabular",
        "explanations": "both",
        "categorical_features": "Yes",
        "train_set_required": "Optional",
        "distributed": "No"
    },
    "SimilarityExplanations": {
        "modeltype": "WhiteBox",
        "modelcategory": "Classification",
        "datatype": ["Tabular", "Text", "Images"],
        "explanations": "local",
        "categorical_features": "Yes",
        "train_set_required": "Yes",
        "distributed": "No"
    }
}