class Algorithm:
    KNN = "KNN"
    XGBOOST = "XGBoost"
    LIGHTGBM = "LightGBM"
    CATBOOST = "CatBoost"
    RANDOM_FOREST = "RandomForest"
    
    @staticmethod
    def from_string(algorithm_str: str) -> str:
        algorithm_str = algorithm_str.lower()
        if algorithm_str in ["knn", "k-nearest neighbors", "k nearest neighbors"]:
            return Algorithm.KNN
        elif algorithm_str in ["xgboost", "xg-boost"]:
            return Algorithm.XGBOOST
        elif algorithm_str in ["lightgbm", "light gbm", "light-boost"]:
            return Algorithm.LIGHTGBM
        elif algorithm_str in ["catboost", "cat-boost"]:
            return Algorithm.CATBOOST
        elif algorithm_str in ["randomforest", "random forest"]:
            return Algorithm.RANDOM_FOREST
        
        return algorithm_str