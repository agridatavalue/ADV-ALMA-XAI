class ExplainerIdentifier:
    model: str
    data: str
    metadata: str
    prediction_target: str

    category: str

    def __init__(
        self, model: str, metadata: str, prediction_target: str, data: str = ""
    ):
        self.data = data
        self.model = model
        self.metadata = metadata
        self.category = ""
        self.prediction_target = prediction_target

    def get_metadata_path(self) -> str:
        return f"{self.model}/{self.prediction_target}_{self.category}/metadata.json".lower()

    def __repr__(self) -> str:
        return f"ExplainerIdentifier(model={self.model} {', metadata='+self.metadata if self.metadata else ''} {', prediction_target='+self.prediction_target if self.prediction_target else ''} {', data='+self.data if self.data else ''})"
