import joblib
from sklearn.pipeline import Pipeline


from ..model import Model


class ScikitLearnModel(Model):
    def load(self, path: str) -> "ScikitLearnModel":
        self.handler = joblib.load(path)
        if isinstance(self.handler, Pipeline):
            self.handler = self.handler.steps[-1][1]

        return self

    @staticmethod
    def supported_frameworks() -> list[str]:
        return ["scikit", "scikit-learn", "sci-kit-learn", "sklearn", "scikitlearn"]
