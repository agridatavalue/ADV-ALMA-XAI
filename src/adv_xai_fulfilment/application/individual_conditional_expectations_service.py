from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import IndividualConditionalExpectations


class IndividualConditionalExpectationService(AbstractModelService):

    def get_data(self, request:ExplainerIdentifier, feature: str) -> IndividualConditionalExpectations:
        context = self.get_context(request)
        
        if feature not in context.model_metadata.feature_names:
            raise Exception(f"Feature {feature} not found in the model")

        return context.model.get_individual_conditional_expectations(context.model_data.x_predict, feature)