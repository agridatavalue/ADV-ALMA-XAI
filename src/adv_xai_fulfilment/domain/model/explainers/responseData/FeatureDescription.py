from .ExplainerResponseData import ExplainerResponseData


class FeatureDescription(ExplainerResponseData):
    name: str
    type: str
    source: str
    description: str

    def __init__(self, name: str, description: str, type: str, source: str):
        self.name = name
        self.type = type
        self.source = source
        self.description = description

    def to_dict(self) -> dict:
        return {
            self.name: self.description,
        }
