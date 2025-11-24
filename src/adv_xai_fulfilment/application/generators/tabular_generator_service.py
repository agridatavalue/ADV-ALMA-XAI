from logger import get_logger
from ...domain.model.data_type import DataType
from ...domain.model.explainers import Explainer
from ...domain.service import ExplainerRetriever
from ...domain.model.model_context import ModelContext
from .abstract_generator_service import AbstractGeneratorService
from ...domain.model.explainers.response_data import FeatureImportance
from ...domain.model.explainers.response_data import ModelPerformanceMetrics
from ...infrastructure.service.explainer_repository_service import (
    ExplainerRepositoryService,
)
from ...domain.service.model_performance_service_component import (
    ModelPerformanceServiceComponent,
)
from ...domain.service.feature_importance_service_component import (
    FeatureImportanceServiceComponent,
)

logger = get_logger()

class TabularGeneratorService(AbstractGeneratorService):
    _explainer_retriever: ExplainerRetriever
    _explainer_service: ExplainerRepositoryService
    _fi_service_comp: FeatureImportanceServiceComponent
    _mpm_service: ModelPerformanceServiceComponent

    def __init__(self):
        super().__init__()
        self._mpm_service = ModelPerformanceServiceComponent()
        self._fi_service_comp = FeatureImportanceServiceComponent()
        self._explainer_retriever = ExplainerRetriever()
        self._explainer_service = ExplainerRepositoryService()

    @staticmethod
    def handled_type() -> DataType:
        return getattr(DataType, 'TABULAR')

    def generate(self, context: ModelContext) -> list:
        context.identifier.category = context.model_metadata.model_category
        logger.debug(f"generating tabular explainers for {str(context.identifier)}")
        
        metrics: ModelPerformanceMetrics = self._mpm_service.get_metrics(
            model_metadata = context.model_metadata,
            model = context.model,
            data = context.model_data,
        )

        logger.debug(
            f"selecting the matching Explainers for model {context.model.__class__.__name__}"
        )
        possible_explainers: list[Explainer] = self._explainer_retriever.get_by_data(
            context
        )
        logger.info(
            f"found {len(possible_explainers)} explainers: {possible_explainers}"
        )

        created_explainers: list[Explainer] = []
        for explainer in possible_explainers:
            logger.debug(
                f"creating {explainer.name} explainer for target {context.identifier.prediction_target}"
            )
            try:
                explainer.build(model=context.model, data=context.model_data)
                self._explainer_service.upload_to(
                    explainer=explainer, identifier=context.identifier
                )
                created_explainers.append(explainer)
            except Exception as e:
                logger.error(
                    f"error building the explainer {explainer.name}: {str(e)}"
                )
        
        logger.debug(
            f"generating feature importance for {str(context.identifier)}"
        )
        feature_importance: FeatureImportance = self._fi_service_comp.generate_data(
            context
        )

        return [feature_importance] + created_explainers + [metrics]
