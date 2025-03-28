from .explainer_response_data import ExplainerResponseData

class ClassLabelSizes(ExplainerResponseData):
    _data: dict

    def __init__(self):
        super().__init__(endpoint='classification-class-label-sizes')
        self._data = {}

    def set_below_cutoff(self, zero: int, one: int) -> 'ClassLabelSizes':
        self._data['below_cutoff'] = { 'class_label_0': zero, 'class_label_1': one }
        return self

    def set_above_cutoff(self, zero: int, one: int) -> 'ClassLabelSizes':
        self._data['above_cutoff'] = { 'class_label_0': zero, 'class_label_1': one }
        return self
    
    def set_total(self, zero: int, one: int) -> 'ClassLabelSizes':
        self._data['total'] = { 'class_label_0': zero, 'class_label_1': one }
        return self

    def to_dict(self) -> dict:
        return self._data

