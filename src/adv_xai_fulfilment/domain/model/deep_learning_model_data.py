import torch
import numpy as np
import torch.nn as nn


from logger import get_logger
from .model_data import ModelData
from .model_metadata_layer import ModelMetaDataLayer

logger = get_logger()

class DeepLearningModelData(ModelData):
    data_predict: np.ndarray
    
    def calculate_federated_y_predict(
        self, 
        model: "Model",
        metadata_layers: list[ModelMetaDataLayer],
    ) -> "ModelData":
        layers = []
        for layer in metadata_layers:
            mapped_types = {
                "Conv1d": nn.Conv1d,
                "ReLU": nn.ReLU,
                "MaxPool1d": nn.MaxPool1d,
                "Flatten": nn.Flatten,
                "Dropout": nn.Dropout,
                "Linear": nn.Linear,
            }
            layers.append(mapped_types[layer.type](**layer.parameters))
            
        sequencial_model = nn.Sequential(*layers)
        
        if self.x_predict.empty:
            self.x_predict = self.data_predict
        
        X_test_tensor = torch.tensor(self.x_predict, dtype=torch.float32).transpose(1, 2)
        y_test_tensor = torch.tensor(self.y_test, dtype=torch.float32)

        with torch.no_grad():
            self._y_predict = sequencial_model(X_test_tensor)
            
        return self

    @property
    def is_empty(self) -> bool:
        return (
            self.data_predict is None
            or self.data_predict.size == 0
            or self.data_train is None
            or self.data_train.empty
        )

    def __repr__(self) -> str:
        return f"DeepLearningModelData(predict_x={self._x_predict}, predict_y={self._y_predict}, image_path={self._image_path})"
    
    