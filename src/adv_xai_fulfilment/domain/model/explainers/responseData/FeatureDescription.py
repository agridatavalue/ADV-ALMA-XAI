from .ExplainerResponseData import ExplainerResponseData


class FeatureDescription(ExplainerResponseData):
    name: str
    type: str
    source: str
    description: str

    def __init__(
        self, name: str = "", description: str = "", type: str = "", source: str = ""
    ):
        super().__init__("feature-description")
        self.name = name
        self.type = type
        self.source = source
        self.description = description

    def to_dict(self) -> dict:
        return {
            self.name: self.description,
        }

    def __repr__(self) -> str:
        str_to_return = f"{self.__class__.__name__}("
        for prop in ["name", "type", "source", "description"]:
            if getattr(self, prop):
                str_to_return += f"{prop}={getattr(self, prop)}, "
        return str_to_return + ")"
