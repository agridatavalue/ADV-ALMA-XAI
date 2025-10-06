import os, sys
import requests
from dotenv import load_dotenv

load_dotenv()

# python integration_tests/verify.py inagro

SERVER_URL = f"http://localhost:{os.getenv('SERVER_PORT')}/"

ALL_DATA = {
    "inagro": {
        "data_for_predict": "ai_flows/CNN_InAgro_2025-09-25_23-22-12/test_dataset/X_test.npy",
        "meta_data": "ai_flows/CNN_InAgro_2025-09-25_23-22-12/metadata.json",
        "model": "ai_flows/CNN_InAgro_2025-09-25_23-22-12/CNN_inagro_20250925_232212.pth",
        "partner": "487",
        "prediction_target": "Net yield (ton/ha marketable",
        "data_for_train": "https://minio.store.platform.agridatavalue.eu/agridatavalue/ai_flows/CNN_InAgro_2025-09-25_23-22-12/training_dataset/"
    },
    "fdml_test": {
        "data_for_predict": "ai_flows/Final_Regression_Test_model_8b43bc2a-47b6-48e1-9d34-372cf0e9475d/datasets/Predict_2025-09-19_08-39-54/data.csv",
        "meta_data": "ai_flows/Final_Regression_Test_model_f17306ab-89b3-4c7d-bfac-3a62f694da01/metadata_air_humidity_final_regression_test_model_20250912_091602.json",
        "model": "ai_flows/Final_Regression_Test_model_f17306ab-89b3-4c7d-bfac-3a62f694da01/air_humidity_final_regression_test_model_20250912_091602.pkl",
        "partner": "487",
        "prediction_target": "Air humidity",
        "data_for_train": "https://minio.store.platform.agridatavalue.eu/agridatavalue/ai_flows/Final_Regression_Test_model_f17306ab-89b3-4c7d-bfac-3a62f694da01/datasets/Train_2025-09-12_09-16-01/data.csv"
    },
    "gradient_boosting_regressor": {
        "data_for_predict": "ai_flows/Greenhouse_Window_Control_8f0cb9b8-d72d-49e6-aef8-93d74829b5d2/datasets/Predict_2025-10-06_12-13-59/data.csv",
        "meta_data": "ai_flows/gradient_boosting_regressor_2025-05-13_14-00-00/metadata_gradient_boosting_regressor.json",
        "model": "ai_flows/gradient_boosting_regressor_2025-05-13_14-00-00/gradient_boosting_regressor.pkl",
        "partner": "c457f78c-d8d6-459b-a0b5-d0dd43fcd6c3",
        "prediction_targets": [
            "Window position side 1 [%]"
        ],
        "data_for_train": "https://minio.store.platform.agridatavalue.eu/agridatavalue/ai_flows/gradient_boosting_regressor_2025-05-13_14-00-00/data/greenhouse_regression.csv"
    }
}

if len(sys.argv) < 2 or sys.argv[1] not in ALL_DATA.keys():
    print(f"Usage: python inagro.py [{'|'.join(ALL_DATA.keys())}]")
    sys.exit(1)


DATA_TO_SEND = ALL_DATA.get(sys.argv[1], {})

response = requests.post(
    f"{SERVER_URL}build", 
    json={
        **DATA_TO_SEND, 
        "prediction_targets": [DATA_TO_SEND.get("prediction_target")],
    }
)
print('>>> build result:', response.json())

# -------------------------------------------
# -------------------------------------------
print("\n\n>>> Starting tests...\n")
print("==== DATA  CARD ====")

data_distribution_response = requests.post(
    f"{SERVER_URL}data-distribution", 
    json=DATA_TO_SEND,
)
print('>>> data_distribution_response:', data_distribution_response.json())
# -------------------------------------------

data_source_type_response = requests.get(
    f"{SERVER_URL}data-source-types?model={DATA_TO_SEND.get('model')}"
)
print('>>> data_source_type_response:', data_source_type_response.json())
# -------------------------------------------

targets_response = requests.post(
    f"{SERVER_URL}targets", 
    json=DATA_TO_SEND,
)
print('>>> targets_response:', targets_response.json())
# -------------------------------------------

# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
print("==== MODEL CARD ====")

classification_class_label_size_response = requests.post(
    f"{SERVER_URL}classification-class-label-sizes", 
    json=DATA_TO_SEND,
)
print('>>> classification_class_label_size_response:', classification_class_label_size_response.json())

# -------------------------------------------
confusion_matrix_response = requests.post(
    f"{SERVER_URL}confusion-matrix", 
    json=DATA_TO_SEND,
)
print('>>> confusion_matrix_response:', confusion_matrix_response.json())

# -------------------------------------------
data_feature_and_average_score_response = requests.post(
    f"{SERVER_URL}data-features-and-average-score", 
    json=DATA_TO_SEND,
)
print('>>> data_feature_and_average_score_response:', data_feature_and_average_score_response.json())

# -------------------------------------------
feature_importance_response = requests.post(
    f"{SERVER_URL}feature-importance", 
    json=DATA_TO_SEND,
)
print('>>> feature_importance_response:', feature_importance_response.json())

# -------------------------------------------
feature_descriptions_response = requests.post(
    f"{SERVER_URL}feature-descriptions", 
    json=DATA_TO_SEND,
)
print('>>> feature_descriptions_response:', feature_descriptions_response.json())

# -------------------------------------------
ice_response = requests.post(
    f"{SERVER_URL}individual-conditional-expectations", 
    json={
        **DATA_TO_SEND, 
        "feature": feature_importance_response.json().get("features", [None])[0]
    }
)
print('>>> ice_response:', ice_response.json())

# -------------------------------------------
lift_curve = requests.post(
    f"{SERVER_URL}lift-curve", 
    json=DATA_TO_SEND,
)
print('>>> lift_curve:', lift_curve.json())

# -------------------------------------------
model_performance_response = requests.post(
    f"{SERVER_URL}model-performance", 
    json=DATA_TO_SEND,
)
print('>>> model_performance_response:', model_performance_response.json())

# -------------------------------------------
model_performance_metrics_response = requests.post(
    f"{SERVER_URL}model-performance-metrics", 
    json=DATA_TO_SEND,
)
print('>>> model_performance_metrics_response:', model_performance_metrics_response.json())

# -------------------------------------------
partial_dependence_response = requests.post(
    f"{SERVER_URL}partial-dependence", 
    json={
        **DATA_TO_SEND, 
        "feature": feature_importance_response.json().get("features", [None])[0]
    },
)
print('>>> partial_dependence_response:', partial_dependence_response.json())
