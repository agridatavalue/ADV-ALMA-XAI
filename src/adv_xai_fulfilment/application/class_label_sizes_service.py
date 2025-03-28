import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

from .confusion_matrix_service import ConfusionMatrixService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import ClassLabelSizes, ConfusionMatrix

class ClassLabelSizesService:
    _confusion_matrix_service: ConfusionMatrixService

    def __init__(self):
        self._confusion_matrix_service = ConfusionMatrixService()

    def get_data(self, expl_id:ExplainerIdentifier) -> ClassLabelSizes:
        cm_obj: ConfusionMatrix = self._confusion_matrix_service.get_data(expl_id)
        cm: pd.DataFrame = cm_obj.data

        total_samples = cm.values.sum()
        actual_open = cm.iloc[0, :][0]
        actual_closed = cm.iloc[0, :][1]
        predicted_open = cm.iloc[1, :][0]
        predicted_closed = cm.iloc[1, :][1]

        return ClassLabelSizes().set_below_cutoff(
            zero=(actual_open / total_samples) * 100, 
            one=(actual_closed / total_samples) * 100
        ).set_above_cutoff(
            zero=(predicted_open / total_samples) * 100, 
            one=(predicted_closed / total_samples) * 100
        ).set_total(
            zero=(actual_open + predicted_open) / total_samples * 100, 
            one=(actual_closed + predicted_closed) / total_samples * 100
        )
