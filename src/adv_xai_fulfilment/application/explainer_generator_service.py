from logger import get_logger
from ..domain.model.model_metadata import ModelMetaData
from .abstract_model_service import AbstractModelService
from ..domain.model.explainer_guide import ExplainerGuide
from ..domain.model.explainers.explainer import Explainer
from .generators import AbstractGeneratorService, generators
from ..domain.model.explainer_metadata import ExplainerMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..infrastructure.service.data_loader_service import DataLoaderService
from ..domain.model.explainers.response_data import ExplainerResponseData
from ..infrastructure.service.model_loader_service import ModelLoaderService
from ..infrastructure.service.metadata_loader_service import MetaDataLoaderService
from ..domain.service.feature_importance_service_component import (
    FeatureImportanceServiceComponent,
)
from ..domain.model.explainers.response_data.explainer_response_data import (
    ExplainerResponseData,
)

logger = get_logger()


class ExplainerGeneratorService(AbstractModelService):
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _metadata_loader_service: MetaDataLoaderService
    _fi_service_comp: FeatureImportanceServiceComponent

    _generators: dict[str, type[AbstractGeneratorService]] = {
        g.handled_type(): g() for g in generators
    }

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._model_loader_service = ModelLoaderService()
        self._metadata_loader_service = MetaDataLoaderService()
        self._fi_service_comp = FeatureImportanceServiceComponent()

    def describe_explainer(
        self, request: ExplainerIdentifier
    ) -> ExplainerGuide:
        logger.debug(f"downloading meta_data {request.metadata_identifier}")
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            expl_id=request
        )
        return ExplainerGuide(meta_data)

    def generate_explainer(self, request: ExplainerIdentifier) -> list[Explainer]:
        context = self.get_context(request)
        
        results: list[ExplainerResponseData] = self._generators[
            context.model_metadata.data_type
        ].generate(context=context)

        expl_metadata = ExplainerMetaData(
            meta_data=context.model_metadata,
            target_name=request.prediction_target,
        ).detect(data=results)

        logger.debug("uploading the explainer metadata")
        self._metadata_loader_service.upload_explainer_metadata(
            metadata=expl_metadata, expl_id=request
        )

        return [r for r in results if isinstance(r, Explainer)]

    def ask_to_explainer(
        self,
        request: str,
        explainer_name: str,
        explainer_identifier: ExplainerIdentifier,
    ):
        explainer: Explainer = self._explainer_retriever.get_by_name(explainer_name)
        partner_data = self._model_loader_service.download_for(
            partner=explainer_identifier.partner.id
        )
        explainer.train_with_partner_data(partner_data)
        return explainer.ask_to_llm(request)
