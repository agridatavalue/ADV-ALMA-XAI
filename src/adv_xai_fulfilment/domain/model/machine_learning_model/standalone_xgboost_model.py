import joblib
from sklearn.pipeline import Pipeline


from ..model import Model


class StandaloneXgBoostModel(Model):
    def load(self, data: dict) -> "StandaloneXgBoostModel":
        self.handler = joblib.load(data.get('path'))
        if isinstance(self.handler, Pipeline):
            self.handler = self.handler.steps[-1][1]

        return self

    @staticmethod
    def supported_frameworks() -> list[str]:
        return [
            "xgboost_standalone", "xgboost standalone", "xg-boost_standalone", 
            "xg-boost-standalone", "xg_boost_standalone", "xgb_standalone"
        ]
    
    def predict(self, X):
        return self.handler.predict(X)
