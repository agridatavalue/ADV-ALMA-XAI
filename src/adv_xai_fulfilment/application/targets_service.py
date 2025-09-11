from .abstract_model_service import AbstractModelService
from ..domain.model.explainers.response_data import Targets
from ..domain.model.explainer_metadata import ExplainerMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier

class TargetsService(AbstractModelService):

    def get_data(self, expl_id: ExplainerIdentifier) -> Targets:
        context = self.get_context(expl_id)
        
        meta_data: ExplainerMetaData = self._metadata_loader_service.load_explainer_metadata(expl_id)
        feature: str = meta_data.feature_importance.get_most_important()

        return Targets().set_x(
            context.model_data.x_train[feature]
        ).set_y(
            real = context.model_data.y_train, 
            predicted = context.model.handler.predict(context.model_data.x_train)
        )
