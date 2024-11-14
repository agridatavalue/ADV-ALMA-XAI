class Errors:
    PILOT_NOT_STRING = TypeError("pilot must be a string")
    MODEL_FILENAME_NOT_STRING = TypeError("model_filename must be a string")
    METADATA_FILENAME_NOT_STRING = TypeError("metadata_filename must be a string")
    REQUEST_NOT_STRING = TypeError("request must be a string")
    EXPLAINER_NAME_NOT_STRING = TypeError("explainer_name must be a string")
    PREDICTION_TARGET_NOT_STRING = TypeError("prediction_target must be a string")
    PREDICTION_TARGET_INDEX_NOT_INT = TypeError("prediction_target_index must be int")

    EXPLAINER_DATA_NOT_EXPLAINER_METADATA = TypeError(
        "explainer_data must be an instance of ExplainerMetaData"
    )
    MODEL_NOT_MODEL = TypeError("model must be an instance of Model")
    DATA_NOT_DICT = TypeError("data must be a dictionary")
    METADATA_NOT_DICT = TypeError("metadata must be a dictionary")

    EXPLAINER_NOT_EXPLAINER = TypeError("explainer must be an instance of Explainer")

    METRICS_NOT_EMPTY = TypeError("Metrics should not be empty")
    METRICS_NOT_DICT = TypeError("Metrics must be a dictionary")

    POSSIBLE_EXPLAINERS_NOT_LIST = TypeError("possible_explainers must be a list")
    POSSIBLE_EXPLAINERS_NOT_EMPTY = TypeError("possible_explainers should not be empty")
    POSSIBLE_EXPLAINERS_ELEMENT_NOT_EXPLAINER = TypeError(
        "All elements in possible_explainers should be of type Explainer"
    )
    PATH_NOT_PICKLE = TypeError("Path must be a pickle file.")

    EXPLAINER_IDENTIFIER_NOT_EXPLAINER_IDENTIFIER = TypeError(
        "explainer_id must be an instance of ExplainerIdentifier"
    )
