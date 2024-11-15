class FeatureDescription:
    name: str
    type: str
    source: str
    description: str

    def __init__(self, name: str, description: str, type: str, source: str):
        self.name = name
        self.type = type
        self.source = source
        self.description = description

    @staticmethod
    def create_from_dict(data: dict) -> "FeatureDescription":
        return FeatureDescription(
            name=data["name"],
            type=data["type"],
            source=data["source"],
            description=data["description"],
        )
