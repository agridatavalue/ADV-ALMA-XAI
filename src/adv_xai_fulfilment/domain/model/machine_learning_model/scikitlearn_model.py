import joblib
from sklearn.pipeline import Pipeline


from ..model import Model


class ScikitLearnModel(Model):
    def load(self, data: dict) -> "ScikitLearnModel":
        self.handler = joblib.load(data.get('path'))
        if isinstance(self.handler, Pipeline):
            self.handler = self.handler.steps[-1][1]

        return self

    @staticmethod
    def supported_frameworks() -> list[str]:
        return ["scikit", "scikit-learn", "sci-kit-learn", "sklearn", "scikitlearn"]
    
    def predict(self, X):
        return self.handler.predict(X)
