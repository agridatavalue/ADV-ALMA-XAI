import os, sys
import requests
from dotenv import load_dotenv

load_dotenv()


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
feature_importance_response = requests.post(
    f"{SERVER_URL}feature-importance", 
    json=DATA_TO_SEND,
)
print('>>> feature-importance response:', feature_importance_response.json())

# -------------------------------------------
partial_dependence_response = requests.post(
    f"{SERVER_URL}partial-dependence", 
    json={**DATA_TO_SEND, "feature": ""},
)
print('>>> partial_dependence response:', partial_dependence_response.json())

# -------------------------------------------
model_performance_response = requests.post(
    f"{SERVER_URL}model-performance", 
    json=DATA_TO_SEND,
)
print('>>> model-performance response:', model_performance_response.json())

# -------------------------------------------
model_performance_metrics_response = requests.post(
    f"{SERVER_URL}model-performance-metrics", 
    json=DATA_TO_SEND,
)
print('>>> model-performance-metrics response:', model_performance_metrics_response.json())

# -------------------------------------------
ice_response = requests.post(
    f"{SERVER_URL}individual-conditional-expectations", 
    json=DATA_TO_SEND,
)
print('>>> ice response:', ice_response.json())

# -------------------------------------------
ice_response = requests.post(
    f"{SERVER_URL}individual-conditional-expectations", 
    json=DATA_TO_SEND,
)
print('>>> ice response:', ice_response.json())

# -------------------------------------------
feature_descriptions_response = requests.post(
    f"{SERVER_URL}feature-descriptions", 
    json=DATA_TO_SEND,
)
print('>>> feature descriptions response:', feature_descriptions_response.json())

# -------------------------------------------
confusion_matrix_response = requests.post(
    f"{SERVER_URL}confusion-matrix", 
    json=DATA_TO_SEND,
)
print('>>> confusion matrix response:', confusion_matrix_response.json())