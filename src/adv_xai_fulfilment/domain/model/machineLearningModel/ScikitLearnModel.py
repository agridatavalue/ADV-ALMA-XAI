from ..Model import Model


class ScikitLearnModel(Model):
    @staticmethod
    def supported_frameworks() -> list[str]:
        return ["scikit-learn", "sci-kit-learn", "sklearn", "scikitlearn"]
