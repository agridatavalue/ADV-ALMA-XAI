import numpy as np
import pandas as pd
from tqdm import tqdm

from ...explainers.response_data import PartialDependence

class PartialDependenceExecutor:
    def process(self, model, X: pd.DataFrame, feature: str) -> PartialDependence:
        num_points = len(X)

        if hasattr(X, "columns"):
            feature_names = X.columns
        else:
            feature_names = [f"Feature {i}" for i in range(X.shape[1])]

        # Convert X to numpy array if it's a DataFrame
        if hasattr(X, "values"):
            X = X.values

        # Get feature index
        if isinstance(feature, str):
            feature_idx = list(feature_names).index(feature)
        else:
            feature_idx = feature
            feature = feature_names[feature_idx]

        # Get feature values range (1st to 99th percentile)
        feature_values = np.linspace(
            np.percentile(X[:, feature_idx], 1),
            np.percentile(X[:, feature_idx], 99),
            num_points,
        )

        # Calculate mean predictions
        predictions = []
        for value in tqdm(feature_values, desc=f"Processing {feature}"):
            X_temp = X.copy()
            X_temp[:, feature_idx] = value
            pred = model.handler.predict(X_temp)
            predictions.append(np.mean(pred))

        return PartialDependence(
            feature_values=feature_values,
            std_effect=np.std(predictions),
            pdp_values=np.array(predictions),
            mean_effect=np.mean(np.abs(np.array(predictions) - np.mean(predictions))),
        )
