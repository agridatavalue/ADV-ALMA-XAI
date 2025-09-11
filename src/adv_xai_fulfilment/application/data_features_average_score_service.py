from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import DataFeaturesAndAverageScore

class DataFeaturesAverageScoreService(AbstractModelService):

    def get_data(self, expl_id:ExplainerIdentifier) -> DataFeaturesAndAverageScore:
        context = self.get_context(expl_id)

        to_ret = DataFeaturesAndAverageScore()
        for f, v in context.model_data.x_predict.mean().to_dict().items():
            to_ret.add_feature(name=f, score=v)
        return to_ret