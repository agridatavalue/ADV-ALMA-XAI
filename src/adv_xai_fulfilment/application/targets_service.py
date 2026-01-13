import pandas as pd
from logger import get_logger

from .abstract_model_service import AbstractModelService
from ..domain.model.explainers.response_data import Targets
from ..domain.model.explainer_metadata import ExplainerMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier

logger = get_logger()

class TargetsService(AbstractModelService):
    def get_data(self, expl_id: ExplainerIdentifier) -> Targets:
        targets = Targets()
        context = self.get_context(expl_id)
        meta_data: ExplainerMetaData = self._metadata_loader_service.load_explainer_metadata(expl_id)
        feature: str = meta_data.feature_importance.get_most_important() if meta_data.feature_importance else ""
        if not feature:
            logger.warning("No feature importance data found; returning empty targets.")
            return targets
    
        if feature not in context.model_data.x_train.columns:
            logger.warning(f"Feature '{feature}' not found in training data; returning empty targets.")
            return targets
    
        x_feature_data = context.model_data.x_train[feature]
        y_real = context.model_data.y_train
        y_pred = context.model.predict(context.model_data.x_train)

        if context.model_metadata.is_regression:
            return targets.set_x(x_feature_data).set_y(real=y_real, predicted=y_pred)

        # Classification case
        y_real_series = pd.Series(y_real)
        y_pred_series = pd.Series(y_pred)

        # Get all class labels (sorted for consistency)
        class_labels = sorted(set(y_real_series.unique()).union(set(y_pred_series.unique())))

        # Count occurrences for each class, ensuring all labels are present
        real_counts = y_real_series.value_counts().reindex(class_labels, fill_value=0).tolist()
        pred_counts = y_pred_series.value_counts().reindex(class_labels, fill_value=0).tolist()

        # Convert class labels to strings (if needed)
        class_labels = [str(label) for label in class_labels]

        return targets.set_x(class_labels).set_y(real=real_counts, predicted=pred_counts)
