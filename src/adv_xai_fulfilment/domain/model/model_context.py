from dataclasses import dataclass

from .model import Model
from .model_data import ModelData
from .model_metadata import ModelMetaData
from .explainer_identifier import ExplainerIdentifier

@dataclass
class ModelContext:
    model: Model
    model_data: ModelData
    model_metadata: ModelMetaData
    identifier: ExplainerIdentifier