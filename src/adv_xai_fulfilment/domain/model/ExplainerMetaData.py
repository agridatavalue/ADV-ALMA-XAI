from src.adv_xai_fulfilment.domain.model.explainers.Explainer import Explainer


class ExplainerMetaData:
    _metrics: dict
    _possible_explainers: list[Explainer]

    def __init__(self, possible_explainers: list[Explainer], metrics: dict):
        assert isinstance(possible_explainers, list)
        assert len(possible_explainers) > 0
        assert all(isinstance(expl, Explainer) for expl in possible_explainers)
        self._possible_explainers = possible_explainers

        assert isinstance(metrics, dict)
        assert len(metrics) > 0
        self._metrics = metrics

    def generate(self) -> dict:
        return {
            "model_metadata": {
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
        }
