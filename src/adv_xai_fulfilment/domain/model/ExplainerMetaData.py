import os

from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.questions.Question import Question
from src.adv_xai_fulfilment.domain.model.explainers.Explainer import Explainer
from src.adv_xai_fulfilment.domain.model.ExplainerIdentifier import ExplainerIdentifier


class ExplainerMetaData:
    _metrics: dict
    _feedback: list[Question]
    _meta_data: ModelMetaData
    _target_name: str
    _feature_importance: dict
    _possible_explainers: list[Explainer]

    def __init__(
        self,
        metrics: dict,
        meta_data: ModelMetaData,
        target_name: str,
        possible_explainers: list[Explainer],
        feature_importance: dict[
            "Feature" : list[str],
            "Importance" : list[float],
            "prediction_target":str,
        ] = {},
        feedback: list[Question] = [],
    ):
        self._possible_explainers = possible_explainers
        self._feature_importance = feature_importance
        self._target_name = target_name
        self._meta_data = meta_data
        self._metrics = metrics
        self._feedback = feedback or []

    @property
    def model_metadata(self) -> ModelMetaData:
        return self._meta_data

    @property
    def feature_importance(
        self,
    ) -> dict[
        "Feature" : list[str],
        "Importance" : list[float],
        "prediction_target":str,
    ]:
        return self._feature_importance

    @property
    def data_are_ok(self) -> bool:
        return (
            isinstance(self._possible_explainers, list)
            and len(self._possible_explainers) > 0
            and all(isinstance(expl, Explainer) for expl in self._possible_explainers)
            and isinstance(self._metrics, dict)
            and len(self._metrics) > 0
        )

    def add_feedback(self, feedback: Question) -> "ExplainerMetaData":
        assert isinstance(feedback, Question), "feedback must be of type Question"
        self._feedback.append(feedback)
        return self

    def get_file_path(self, expl_id: ExplainerIdentifier) -> str:
        if not expl_id.category:
            expl_id.category = "regression"

        return f"{expl_id.model}/{expl_id.prediction_target}_{expl_id.category}/metadata.json".lower()

    def get_locale_file_path(self, expl_id: ExplainerIdentifier) -> str:
        return os.path.join(
            os.getenv("TEMP"), expl_id.model, expl_id.pilot.id, "metadata.json"
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
                "performance_metrics": self._metrics,
                "feature_importance": self._feature_importance,
            },
            "explainer_metadata": {
                "explainers_identified": [
                    expl.name for expl in self._possible_explainers
                ],
                "explanation_method": ["Feature importance", "Model performance"],
                "scope_of_explanation": ["Local", "Global"],
                "vizualization type": ["barplot", "scaterplot"],
            },
            "compliance_and_ethical_considerations": {
                "Rights_for_explanation": "XAI framwork caters to explain and respect the rights of individuals, coopratives and stakholders as outlined in GDPR including rights for explanation",
                "bias_and_fairness": "No significant biases detected during fairness assessment",
                "Lawful_bases_of_data_processing": "",
                "Data_security": "",
                "regulatory_compliance": "Compliant with GDPR and local regulations",
            },
            "feedback_and_improvements": [f.to_dict() for f in self._feedback],
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
                string += f"{attr}={getattr(self, attr)}, "
        return string + ")"
