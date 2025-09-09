from logger import get_logger
from ...domain.model.model import Model
from ...domain.model.data_type import DataType
from ...domain.model.model_data import ModelData
from ...domain.model.explainers import Explainer
from ...domain.service import ExplainerRetriever
from ...domain.model.model_metadata import ModelMetaData
from .abstract_generator_service import AbstractGeneratorService
from ...domain.model.explainer_identifier import ExplainerIdentifier
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

    def generate(
        self,
        *,
        request: ExplainerIdentifier,
        meta_data: ModelMetaData,
        selected_model: Model,
        data: ModelData,
    ) -> list:
        logger.debug(f"generating tabular explainers for {str(request)}")
        if not request.prediction_target:
            request.prediction_target = meta_data.first_target_name
            logger.debug(
                f"prediction target not provided, using the first target: {request.prediction_target}"
            )

        metrics:ModelPerformanceMetrics = self._mpm_service.get_metrics(
            prediction_target=request.prediction_target,
            model_metadata=meta_data,
            model=selected_model,
            data=data,
        )

        logger.debug(
            f"selecting the matching Explainers for model {selected_model.__class__.__name__}"
        )
        possible_explainers: list[Explainer] = self._explainer_retriever.get_by_data(
            selected_model, meta_data
        )
        logger.info(
            f"found {len(possible_explainers)} explainers: {possible_explainers}"
        )

        created_explainers: list[Explainer] = []
        for explainer in possible_explainers:
            logger.debug(
                f"creating {explainer.name} explainer for target {request.prediction_target}"
            )
            try:
                explainer.build(model=selected_model, data=data)
                self._explainer_service.upload_to(
                    explainer=explainer, identifier=request
                )
                created_explainers.append(explainer)
            except Exception as e:
                logger.error(
                    f"error building the explainer {explainer.name}: {str(e)}", exc_info=True
                )
        
        feature_importance: FeatureImportance = self._fi_service_comp.generate_data(
            request
        )

        return [feature_importance] + created_explainers + [metrics]
