from src.adv_xai_fulfilment.domain.model.ModelMetaData import ModelMetaData
from src.adv_xai_fulfilment.domain.model.explainers.Explainer import Explainer


class ExplainerMetaData:
    _metrics: dict
    _meta_data: ModelMetaData
    _target_name: str
    _possible_explainers: list[Explainer]

    def __init__(
        self,
        metrics: dict,
        meta_data: ModelMetaData,
        target_name: str,
        possible_explainers: list[Explainer],
    ):
        self._possible_explainers = possible_explainers
        self._target_name = target_name
        self._meta_data = meta_data
        self._metrics = metrics

    @property
    def data_are_ok(self) -> bool:
        return (
            isinstance(self._possible_explainers, list)
            and len(self._possible_explainers) > 0
            and all(isinstance(expl, Explainer) for expl in self._possible_explainers)
            and isinstance(self._metrics, dict)
            and len(self._metrics) > 0
        )

    def to_dict(self) -> dict:
        return {
            "model_metadata": {
                "subjectname": self._meta_data.subject_name,
                "targetname": self._target_name,
                "modelcategory": self._meta_data.model_category,
                "explaineed_model_name": "neuralnetwork",
                "framework": ["Tensorflow", "pytorch", "scikit"],
                "training_data_summary": "set with 100,000 instances and 20 features and 3 targets",
                "hyperparameters": {
                    "n_neurons": 100,
                    "activation_fun": "Relu",
                    "n_parameters": 100,
                },
                "performance_metrics": self._metrics,
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
            "feedback_and_improvements": {},
        }
