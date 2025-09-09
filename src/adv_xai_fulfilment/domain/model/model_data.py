import pandas as pd

class ModelData:
    _x_predict: pd.DataFrame
    _y_predict: pd.DataFrame
    
    _x_train: pd.DataFrame
    _y_train: pd.DataFrame
    _predicted_y_train: pd.DataFrame
    _image_path: str

    def __init__(self):
        self._x_train = None
        self._y_train = None
        self._x_predict = None
        self._y_predict = None
        self._predicted_y_train = None
        self._image_path = ''
    
    # --------------------------------------------------------------
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
    def y_predict(self) -> pd.DataFrame:
        return self._y_predict
    
    @y_predict.setter
    def y_predict(self, y_predict: pd.DataFrame):
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
        assert isinstance(image, str)
        self._image_path = image

    def get_y_for_prediction_target(self, target: int) -> pd.Series:
        if self._y_predict is None or self._y_predict.empty:
            return pd.Series(dtype=float)
        return self._y_predict.iloc[:, target]

    
    def y_predict_is_empty(self) -> bool:
        return self._y_predict is None or self._y_predict.empty
    
    def y_train_is_empty(self) -> bool:
        return self._y_train is None or self._y_train.empty
    
    @property
    def is_empty(self) -> bool:
        return self._x_predict is None or self._y_predict is None or self._x_predict.empty or self._y_predict.empty

    def __repr__(self) -> str:
        return f"ModelData(predict_x={self._x_predict}, predict_y={self._y_predict}, image_path={self._image_path})"

    # --------------------------------------------------------------
    
    def remove_columns_not_in_model(self, feature_names: list[str]) -> "ModelData":
        if self._x_predict is not None and not self._x_predict.empty:
            cols_to_remove = [col for col in self._x_predict.columns if col not in feature_names]
            if cols_to_remove:
                self._x_predict = self._x_predict.drop(columns=cols_to_remove)
        
        if self._x_train is not None and not self._x_train.empty:
            cols_to_remove = [col for col in self._x_train.columns if col not in feature_names]
            if cols_to_remove:
                self._x_train = self._x_train.drop(columns=cols_to_remove)
        
        return self
    
    # --------------------------------------------------------------
    
    @property
    def x(self) -> pd.DataFrame:
        """DEPRECATED, use x_predict instead"""
        return self._x_predict

    @x.setter
    def x(self, x: pd.DataFrame):
        """DEPRECATED, use x_predict instead"""
        self._x_predict = x

    @property
    def y(self) -> pd.DataFrame:
        """DEPRECATED, use y_predict instead"""
        return self._y_predict

    @y.setter
    def y(self, y: pd.DataFrame):
        """DEPRECATED, use y_predict instead"""
        self._y_predict = y
    
    def y_is_empty(self) -> bool:
        """DEPRECATED, use y_predict_is_empty instead"""
        return self._y_predict is None or self._y_predict.empty