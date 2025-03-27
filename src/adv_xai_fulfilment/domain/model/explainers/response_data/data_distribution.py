from .explainer_response_data import ExplainerResponseData

class DataDistribution(ExplainerResponseData):
    _bin_edges: list[float]
    _counts: list[float]

    def __init__(self):
        super().__init__(endpoint='data-distribution')

    def set_bin_edges(self, bin_edges: list[float]) -> "DataDistribution":
        assert isinstance(bin_edges, list), "bin_edges must be a list"
        
        if all(isinstance(edge, list) or isinstance(edge, tuple) for edge in bin_edges):
            bin_edges = sum([list(e) for e in bin_edges], [])

        self._bin_edges = bin_edges
        return self
    
    def set_counts(self, counts: list[float]) -> "DataDistribution":
        assert isinstance(counts, list), "counts must be a list"

        self._counts = counts
        return self

    def to_dict(self) -> dict:
        return {
            'y_axis_values': self._counts,
            'x_axis_values': self._bin_edges,
        }