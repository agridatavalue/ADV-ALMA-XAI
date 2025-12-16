from .explainer_response_data import ExplainerResponseData

class ModelSummary(ExplainerResponseData):
    _data: dict 
    
    def __init__(self):
        super().__init__(endpoint='get_summary')
        self._data = {}
        
    def add_explanation(self, summary: str) -> 'ModelSummary':
        self._data['summary_text'] = summary
        return self
        
    def to_dict(self) -> dict:
        return self._data