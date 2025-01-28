import joblib

from ..Model import Model


class ScikitLearnModel(Model):
    def load(self, path: str) -> "ScikitLearnModel":
        # self.handler = pickle.load(open(path, "rb"))
        self.handler = joblib.load(path)
        return self

    @staticmethod
    def supported_frameworks() -> list[str]:
        return ["scikit", "scikit-learn", "sci-kit-learn", "sklearn", "scikitlearn"]
