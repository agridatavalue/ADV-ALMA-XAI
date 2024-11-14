import pickle

from ..Model import Model


class ScikitLearnModel(Model):
    def load(self, path: str) -> "ScikitLearnModel":
        self.handler = pickle.load(open(path, "rb"))
        return self

    @staticmethod
    def supported_frameworks() -> list[str]:
        return ["scikit-learn", "sci-kit-learn", "sklearn", "scikitlearn"]
