from .explainer_response_data import ExplainerResponseData


class Heatmap(ExplainerResponseData):
    _heatmap_filepaths: list[str]

    def __init__(self):
        super().__init__(endpoint="heatmap")
        self._heatmap_filepaths = []

    @property
    def is_empty(self) -> bool:
        return len(self._heatmap_filepaths) == 0

    def add(self, heatmap: str):
        if not isinstance(heatmap, str):
            raise Exception("Heatmap must be a string")
        
        self._heatmap_filepaths.append(heatmap)
        return self

    @property
    def heatmaps(self) -> list[str]:
        return self._heatmap_filepaths

    def to_dict(self) -> dict:
        return self._heatmap_filepaths