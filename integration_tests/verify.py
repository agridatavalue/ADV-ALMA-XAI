import os, sys
import logging
import requests

from dotenv import load_dotenv
from colorlog import ColoredFormatter


# Create a logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Create a console handler
handler = logging.StreamHandler()

# Define colorized format
formatter = ColoredFormatter(
    "%(log_color)s[%(levelname)s]%(reset)s %(message_log_color)s%(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
    secondary_log_colors={'message': { 'ERROR': 'red', 'CRITICAL': 'bold_red' }},
    style='%'
)

handler.setFormatter(formatter)
logger.addHandler(handler)

load_dotenv()

# python integration_tests/verify.py inagro

SERVER_URL = f"http://localhost:{os.getenv('SERVER_PORT')}/"

ALL_DATA = {
    "iso": {
        "data_for_predict": "data_temp/ts_isolation_forest/Calving_activity_5051_20250709_094549.xlsx",
        "meta_data": "data_temp/ts_isolation_forest/metadata_isolation_forest_timeseries.json",
        "model": "data_temp/ts_isolation_forest/iso.pkl",
        "partner": "487",
        "data_for_train": "data_temp/ts_isolation_forest/Calving_activity_3063_20250709_094549_train.xlsx"
    },
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
        "data_for_predict": "ai_flows/Greenhouse_Window_Control_775e9b27-0660-4d3a-b7ff-7b051773039b/datasets/Predict_2025-10-09_19-53-42/data.csv",
        "meta_data": "ai_flows/platform_models/gradient_boosting_regressor/metadata_gradient_boosting_regressor.json",
        "model": "ai_flows/platform_models/gradient_boosting_regressor/gradient_boosting_regressor.pkl",
        "partner": "c457f78c-d8d6-459b-a0b5-d0dd43fcd6c3",
        "prediction_targets": [
            "Window position side 1 [%]"
        ],
        "data_for_train": "https://minio.store.platform.agridatavalue.eu/agridatavalue/ai_flows/platform_models/gradient_boosting_regressor/data/temp_greenhouse_regression_norm.csv"
    },
    "random_forest_classifier": {
        "data_for_predict": "ai_flows/random_forest_clf_2025-05-13_14-00-00/data/prediction_data.csv",
        "meta_data": "ai_flows/random_forest_clf_2025-05-13_14-00-00/metadata_random_forest_clf.json",
        "model": "ai_flows/random_forest_clf_2025-05-13_14-00-00/random_forest_clf.pkl",
        "partner": "c457f78c-d8d6-459b-a0b5-d0dd43fcd6c3",
        "prediction_targets": [
            "Window"
        ],
        "data_for_train": "https://minio.store.platform.agridatavalue.eu/agridatavalue/ai_flows/random_forest_clf_2025-05-13_14-00-00/data/greenhouse_classification.csv"
    },
    "olive_fruit_fly": {
        "data_for_predict": "ai_flows/user_flows/Fruit_Fly_Infestation_Risk_Classifier/27bc8b49-6e3b-4b5a-9867-18fe6b20f0b8/datasets/Predict_2025-11-04_10-25-17/normalized_data.csv",
        "data_for_train": "ai_flows/platform_models/fruit_fly_infestation_risk_classifier/data/29_09_2025_risk_train_norm.csv",
        "meta_data": "ai_flows/platform_models/fruit_fly_infestation_risk_classifier/oliveFruitflyRiskOfinfestation.json",
        "model": "ai_flows/platform_models/fruit_fly_infestation_risk_classifier/logisticRegressionOliveFruitflyRiskOfInfestation.pkl",
        "partner": "7ac636e5-0b6a-4d0f-8a8f-962c4fe68ebf",
        "prediction_targets": [
            "target_binary_high_risk"
        ]
    }
}

if len(sys.argv) < 2 or sys.argv[1] not in ALL_DATA.keys():
    logger.error(f"Usage: python verify.py [{'|'.join(ALL_DATA.keys())}]")
    sys.exit(1)


DATA_TO_SEND = ALL_DATA.get(sys.argv[1], {})

try:
    build_response = requests.post(
        f"{SERVER_URL}build", 
        json={
            **DATA_TO_SEND, 
            "prediction_targets": [DATA_TO_SEND.get("prediction_target")],
        }
    )
    json_data = build_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"build error: {json_data}")
    else:
        logger.info(f"build result: {json_data}")
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")

# -------------------------------------------
# -------------------------------------------
logger.info(">>> Starting tests...")
logger.info("==== DATA  CARD ====")

try:
    data_distribution_response = requests.post(
        f"{SERVER_URL}data-distribution", json=DATA_TO_SEND
    )
    json_data = data_distribution_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"data_distribution error: {json_data}")
    else:
        logger.info(f"data_distribution response: {json_data}")
    
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
# -------------------------------------------

try:
    data_source_type_response = requests.get(
        f"{SERVER_URL}data-source-types?model={DATA_TO_SEND.get('model')}"
    )
    json_data = data_source_type_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"data_source_type error: {json_data}")
    else:
        logger.info(f'data_source_type response: {json_data}')
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
# -------------------------------------------

try:
    targets_response = requests.post(
        f"{SERVER_URL}targets", json=DATA_TO_SEND
    )
    json_data = targets_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"targets error: {json_data}")
    else:
        logger.info(f'targets response: {json_data}')
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
# -------------------------------------------

# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
logger.info("==== MODEL CARD ====")

try:
    classification_class_label_size_response = requests.post(
        f"{SERVER_URL}classification-class-label-sizes", json=DATA_TO_SEND
    )
    json_data = classification_class_label_size_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"classification_class_label_size error: {json_data}")
    else:
        logger.info(f'classification_class_label_size response: {json_data}')
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
    
# -------------------------------------------
try:
    confusion_matrix_response = requests.post(
        f"{SERVER_URL}confusion-matrix", json=DATA_TO_SEND
    )
    json_data = confusion_matrix_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"confusion_matrix error: {json_data}")
    else:
        logger.info(f'confusion_matrix response: {json_data}')
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
    
# -------------------------------------------
try:
    data_feature_and_average_score_response = requests.post(
        f"{SERVER_URL}data-features-and-average-score", json=DATA_TO_SEND
    )
    json_data = data_feature_and_average_score_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"data_feature_and_average_score error: {json_data}")
    else:
        logger.info(f'data_feature_and_average_score response: {json_data}')
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
    
# -------------------------------------------
feature_importance_response = None
try:
    feature_importance_response = requests.post(
        f"{SERVER_URL}feature-importance", json=DATA_TO_SEND
    )
    json_data = feature_importance_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"feature_importance error: {json_data}")
    else:
        logger.info(f'feature_importance response: {json_data}')
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
    
# -------------------------------------------
try:
    feature_descriptions_response = requests.post(
        f"{SERVER_URL}feature-descriptions", json=DATA_TO_SEND
    )
    json_data = feature_descriptions_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"feature_descriptions error: {json_data}")
    else:
        logger.info(f'feature_descriptions response: {json_data}')
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
    
# -------------------------------------------
try:
    ice_response = requests.post(
        f"{SERVER_URL}individual-conditional-expectations", 
        json={
            **DATA_TO_SEND, 
            "feature": feature_importance_response.json().get("features", [None])[0]
        }
    )
    json_data = ice_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"ice result error: {json_data}")
    else:
        logger.info(f'ice response: {json_data}')
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
    
# -------------------------------------------
try:
    lift_curve = requests.post(f"{SERVER_URL}lift-curve", json=DATA_TO_SEND)
    json_data = lift_curve.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"lift_curve error: {json_data}")
    else:
        logger.info(f'lift_curve response: {json_data}')
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
    
# -------------------------------------------
try:
    model_performance_response = requests.post(
        f"{SERVER_URL}model-performance", json=DATA_TO_SEND
    )
    json_data = model_performance_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"model_performance error: {json_data}")
    else:
        logger.info(f'model_performance response: {json_data}')
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
    
# -------------------------------------------
try:
    model_performance_metrics_response = requests.post(
        f"{SERVER_URL}model-performance-metrics", json=DATA_TO_SEND
    )
    json_data = model_performance_metrics_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"model_performance_metrics error: {json_data}")
    else:
        logger.info(f'model_performance_metrics response: {json_data}')
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
    
# -------------------------------------------
try:
    partial_dependence_response = requests.post(
        f"{SERVER_URL}partial-dependence", 
        json={
            **DATA_TO_SEND, 
            "feature": feature_importance_response.json().get("features", [None])[0]
        },
    )
    json_data = partial_dependence_response.json()
    
    if "error" in json_data or "status" in json_data and "error" in str(json_data["status"]).lower():
        logger.error(f"partial_dependence error: {json_data}")
    else:
        logger.info(f'partial_dependence response: {json_data}')
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")