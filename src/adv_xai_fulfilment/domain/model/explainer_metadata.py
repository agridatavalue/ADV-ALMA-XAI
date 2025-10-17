import os
from typing import Optional

from .partner import Partner 
from .questions import Feedback
from .model_metadata import ModelMetaData
from .explainers.explainer import Explainer
from .explainer_identifier import ExplainerIdentifier
from .explainers.response_data import ModelPerformanceMetrics
from .explainers.response_data import FeatureImportance, Heatmap


class ExplainerMetaData:
    _metrics: Optional[ModelPerformanceMetrics]
    _target_name: str
    _feedbacks: list[Feedback]
    _meta_data: ModelMetaData
    _heatmap_images: Optional[Heatmap]
    _feature_importance: Optional[FeatureImportance]
    _possible_explainers: list[Explainer]

    def __init__(
        self,
        *,
        meta_data: ModelMetaData,
        target_name: str,
        metrics: Optional[ModelPerformanceMetrics] = None,
        possible_explainers: list[Explainer] = [],
        feature_importance: Optional[FeatureImportance] = None,
        feedbacks: list[Feedback] = [],
        heatmap_images: Optional[Heatmap] = None,
    ):
        self._possible_explainers = possible_explainers
        self._feature_importance = feature_importance
        self._heatmap_images = heatmap_images
        self._target_name = target_name
        self._feedbacks = feedbacks
        self._meta_data = meta_data
        self._metrics = metrics

    def detect(self, data: list) -> "ExplainerMetaData":
        def find(data, type):
            return next((item for item in data if isinstance(item, type)), None)

        self._metrics = find(data, ModelPerformanceMetrics)
        self._heatmap_images = find(data, Heatmap)
        self._feature_importance = find(data, FeatureImportance)
        self._possible_explainers = [
            explainer
            for sublist in data
            if isinstance(sublist, list)
            for explainer in sublist
            if isinstance(explainer, Explainer)
        ]

        return self

    @property
    def model_metadata(self) -> ModelMetaData:
        return self._meta_data

    @property
    def heatmap(self) -> Optional[Heatmap]:
        return self._heatmap_images

    @property
    def feature_importance(self) -> Optional[FeatureImportance]:
        return self._feature_importance

    def add_feedback(self, feedback: Feedback) -> "ExplainerMetaData":
        if not isinstance(feedback, Feedback):
            raise ValueError(f"feedback must be of type Feedback, got {type(feedback)}")
        
        self._feedbacks.append(feedback)
        return self
    
    def get_all_feedback(self, filter_by: Optional[Partner]) -> list[Feedback]:
        if isinstance(filter_by, Partner):
            return [f for f in self._feedbacks if f.partner.id == filter_by.id]
        
        return self._feedbacks

    def get_locale_file_path(self, expl_id: ExplainerIdentifier) -> str:
        return os.path.join(
            os.getenv("TEMP", '/tmp'), expl_id.model, expl_id.partner.id, "metadata.json"
        )

    def to_dict(self) -> dict:
        return {
            "model_metadata": {
                "subjectname": self._meta_data.subject_name if self._meta_data else "",
                "targetname": self._target_name,
                "modelcategory": (
                    self._meta_data.model_category if self._meta_data else ""
                ),
                "explaineed_model_name": "neuralnetwork",
                "framework": ["Tensorflow", "pytorch", "scikit"],
                "training_data_summary": "set with 100,000 instances and 20 features and 3 targets",
                "hyperparameters": {
                    "n_neurons": 100,
                    "activation_fun": "Relu",
                    "n_parameters": 100,
                },
                "performance_metrics": self._metrics.to_dict() if self._metrics else {},
                "feature_importance": (
                    self._feature_importance.to_dict()
                    if self._feature_importance
                    else {}
                ),
            },
            "explainer_metadata": {
                "explainers_identified": [
                    expl.name for expl in self._possible_explainers
                ],
                "explanation_method": ["Feature importance", "Model performance"],
                "scope_of_explanation": ["Local", "Global"],
                "vizualization type": ["barplot", "scaterplot"],
                "heatmaps": (
                    self._heatmap_images.to_dict() if self._heatmap_images else []
                ),
            },
            "compliance_and_ethical_considerations": {
                "Rights_for_explanation": "XAI framwork caters to explain and respect the rights of individuals, coopratives and stakholders as outlined in GDPR including rights for explanation",
                "bias_and_fairness": "No significant biases detected during fairness assessment",
                "Lawful_bases_of_data_processing": "",
                "Data_security": "",
                "regulatory_compliance": "Compliant with GDPR and local regulations",
            },
            "feedback_and_improvements": [f.to_dict() for f in self._feedbacks],
        }

    def __repr__(self) -> str:
        string = f"ExplainerMetaData("
        for attr in [
            "_meta_data",
            "_target_name",
            "_possible_explainers",
            "_metrics",
            "_feature_importance",
        ]:
            if getattr(self, attr):
                try:
                    string += f"{attr}={getattr(self, attr)}, "
                except: pass
        return string + ")"
