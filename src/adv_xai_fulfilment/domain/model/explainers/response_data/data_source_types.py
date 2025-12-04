from .explainer_response_data import ExplainerResponseData

class DataSourceTypes(ExplainerResponseData):
    _data: dict[str, int]
    
    def __init__(self):
        super().__init__("data-source-types")
        self._data = {}
        
    def add_source_type(self, source_type: str, count: int) -> "DataSourceTypes":
        if not source_type in self._data:
            self._data[source_type] = 0
        self._data[source_type] += count
        return self
    
    def to_dict(self) -> list[dict[str, int]]:
        return [{"type": k, "value": v} for k, v in self._data.items()]