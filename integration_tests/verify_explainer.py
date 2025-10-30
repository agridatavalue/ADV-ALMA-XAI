import pickle
import os, sys
from dotenv import load_dotenv

sys.path.append("/home/mirko/PROGETTI/ADV/adv-xai-fulfilment")


load_dotenv()

# python integration_tests/verify_explainer.py data_temp/gradient_boosting_regressor.pkl/c457f78c-d8d6-459b-a0b5-d0dd43fcd6c3/PartialDependence.pkl

EXPLAINER_PATH = sys.argv[1]

if len(sys.argv) < 2 or not sys.argv[1]:
    print(f"Usage: python verify_explainer.py <explainer_path>")
    sys.exit(1)
    
if not os.path.exists(EXPLAINER_PATH):
    print(f"Explainer path {EXPLAINER_PATH} does not exist.")
    sys.exit(1)
    
explainer = pickle.load(open(EXPLAINER_PATH, "rb"))



for attr in dir(explainer):
    if attr.startswith("_"):
        continue
    
    print(f"{attr}: {getattr(explainer, attr)}")
    
# ----------------------------------------------------

print('#' * 80)

import pandas as pd

data = pd.read_csv('data_temp/gradient_boosting_regressor.pkl/c457f78c-d8d6-459b-a0b5-d0dd43fcd6c3/data_for_train/temp_greenhouse_regression_norm.csv')
data = data.drop(columns=['Window position side 1 [%]'])
print(data.head())


explain = explainer.explain(X=data.values, features=[0], grid_resolution=50)
print(explain.data)

alibi_results = {}
for feature in data.columns:
    # Get feature index if feature is a string
    if isinstance(feature, str):
        feature_idx = list(data.columns).index(feature)
    else:
        feature_idx = feature
    
    # Calculate PD
    explanation = explainer.explain(
        X=data.values if hasattr(data, 'values') else data,
        features=[feature_idx],
        grid_resolution=50  # Match sklearn's resolution
    )
    
    alibi_results[feature] = {
        'grid_values': explanation.feature_values[0],
        'average': explanation.pd_values[0],
        'feature_deciles': explanation.feature_deciles[0] if hasattr(explanation, 'feature_deciles') else None
    }
    
    print(f"\nFeature: {feature}")
    print(f"Grid shape: {explanation.feature_values[0].shape}")
    print(f"PDP shape: {explanation.pd_values[0].shape}")
print(alibi_results )

# ===== VISUALIZATION =====
import matplotlib.pyplot as plt
import numpy as np

features = list(alibi_results.keys())
print("\n" + "=" * 50)
print("Creating plots...")

fig, axes = plt.subplots(len(features), 1, figsize=(10, 5 * len(features)))
if len(features) == 1:
    axes = [axes]

for idx, feature in enumerate(features):
    ax = axes[idx]
    
    # Plot Alibi PDP (flatten to ensure 1D arrays)
    alibi_grid = np.asarray(alibi_results[feature]['grid_values']).flatten()
    alibi_pd = np.asarray(alibi_results[feature]['average']).flatten()
    
    ax.plot(alibi_grid, alibi_pd,
            label='Alibi PDP', marker='o', linewidth=2)
    
    ax.set_xlabel(f'{feature}')
    ax.set_ylabel('Partial Dependence')
    ax.set_title(f'Partial Dependence Plot: {feature}')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\nDone!")
"""
import pandas as pd
from sklearn.inspection import PartialDependenceDisplay

# Assuming gb_regr is your trained model and X is your feature set
# Get the feature names from the DataFrame
feature_names = data.columns

# Create the Partial Dependence Plot for all features
fig, ax = plt.subplots(figsize=(15, 10))


PartialDependenceDisplay.from_estimator(model, data.values, features=range(data.shape[1]), feature_names=feature_names, ax=ax)
plt.show()
"""