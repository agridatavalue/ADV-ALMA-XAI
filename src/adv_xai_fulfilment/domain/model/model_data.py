import shap
import torch
import numpy as np
import pandas as pd
import torch.nn as nn
from sklearn.model_selection import train_test_split


from logger import get_logger
from .model_category import ModelCategory
from .model_metadata_layer import ModelMetaDataLayer

logger = get_logger()

class ModelData:
    _x_test: pd.DataFrame 
    _y_test: pd.DataFrame 
    _x_predict: pd.DataFrame # comes from data csv file (test data)
    _y_predict: np.ndarray  # comes from model prediction
    
    _x_train: pd.DataFrame # comes from data csv file
    _y_train: pd.DataFrame
    
    data_train: pd.DataFrame
    data_predict: pd.DataFrame
    data_validation: pd.DataFrame
    
    _predicted_y_train: pd.DataFrame
    _image_path: str

    def __init__(self):
        self._x_test = None
        self._y_test = None
        self._x_train = None
        self._y_train = None
        self._x_predict = None
        self._y_predict = None
        self._predicted_y_train = None
        self._image_path = ''
        
        self.data_train = pd.DataFrame()
        self.data_predict = pd.DataFrame()
        self.data_validation = pd.DataFrame()
        
    def calculate_x_and_y_predict_and_x_and_y_train(
        self, 
        model: "Model",
        feature_names: list[str], 
        model_category: ModelCategory,
        target_name: str = "",
    ) -> "ModelData":
        if self.data_predict is not None and not self.data_predict.empty:            
            cols_to_remove = [col for col in self.data_predict.columns if col not in feature_names]
            if cols_to_remove:
                logger.debug(f"predict - Removing columns not in feature names: {cols_to_remove}")
                self._x_predict = self.data_predict.drop(columns=cols_to_remove)
                self._x_predict = self._x_predict[feature_names]
                
        if self.data_train is not None and not self.data_train.empty:
            cols_to_remove = [col for col in self.data_train.columns if col not in feature_names]
            X = self.data_train.drop(columns=cols_to_remove)
            y = self.data_train[target_name]
            if ModelCategory.is_classification(str(model_category)):
                _, X_test, _, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
            else:
                _, X_test, _, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
            self._y_test = y_test
            self._y_predict = model.predict(X_test)
            
            # from sklearn.preprocessing import MinMaxScaler
            # scaler = MinMaxScaler()
            # test_data_norm = pd.DataFrame(scaler.fit_transform(self.x_predict), columns=self.x_predict.columns)
            # self._y_predict = model.predict(test_data_norm)
            
            self._y_train = self.data_train[target_name] if target_name in self.data_train.columns else self.data_train
            if cols_to_remove:
                logger.debug(f"train - Removing columns not in feature names: {cols_to_remove}")
                self._x_train = self.data_train.drop(columns=cols_to_remove)
                self._x_train = self._x_train[feature_names]
                
        return self
    
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
            
    # --------------------------------------------------------------
    @property
    def x_test(self) -> pd.DataFrame:
        return self._x_test if self._x_test is not None else pd.DataFrame()
    
    @property
    def y_test(self) -> pd.DataFrame:
        return self._y_test if self._y_test is not None else pd.DataFrame()
    
    @property
    def predicted_y_train(self) -> pd.DataFrame:
        return self._predicted_y_train
    
    @predicted_y_train.setter
    def predicted_y_train(self, predicted_y_train: pd.DataFrame):
        self._predicted_y_train = predicted_y_train
        
    # --------------------------------------------------------------
    @property
    def x_predict(self) -> pd.DataFrame:
        return self._x_predict if self._x_predict is not None else pd.DataFrame()
    
    @x_predict.setter
    def x_predict(self, x_predict: pd.DataFrame):
        self._x_predict = x_predict
        
    @property
    def y_predict(self) -> np.ndarray:
        return self._y_predict
    
    @y_predict.setter
    def y_predict(self, y_predict: np.ndarray):
        self._y_predict = y_predict

    # --------------------------------------------------------------
    @property
    def x_train(self) -> pd.DataFrame:
        return self._x_train if self._x_train is not None else pd.DataFrame()
    
    @x_train.setter
    def x_train(self, x_train: pd.DataFrame):
        self._x_train = x_train
        
    @property
    def y_train(self) -> pd.DataFrame:
        return self._y_train
    
    @y_train.setter
    def y_train(self, y_train: pd.DataFrame):
        self._y_train = y_train

    # --------------------------------------------------------------
    @property
    def image_path(self) -> str:
        return self._image_path

    @image_path.setter
    def image_path(self, image: str):
        if not isinstance(image, str):
            raise ValueError("Image path must be a string")
        self._image_path = image

    @property
    def is_empty(self) -> bool:
        return self.data_predict is None or self.data_train is None or (self.data_predict.empty and self.data_train.empty)

    def __repr__(self) -> str:
        return f"ModelData(predict_x={self._x_predict}, predict_y={self._y_predict}, image_path={self._image_path})"
    
    