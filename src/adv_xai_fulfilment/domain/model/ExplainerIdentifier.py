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
        string_to_return = f"ExplainerIdentifier(model={self.model}"
        for attr in ["category", "data", "metadata", "prediction_target"]:
            if getattr(self, attr):
                string_to_return += f", {attr}={getattr(self, attr)}"
        return string_to_return + ")"
