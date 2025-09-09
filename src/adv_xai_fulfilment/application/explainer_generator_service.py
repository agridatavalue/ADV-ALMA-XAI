from logger import get_logger
from ..domain.model.model import Model
from ..infrastructure.constants import Errors
from ..domain.model.model_data import ModelData
from ..domain.model.model_metadata import ModelMetaData
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


class ExplainerGeneratorService:
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
    ) -> list[ExplainerResponseData]:
        logger.debug(f"downloading meta_data {request.metadata_identifier}")
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            expl_id=request
        )
        return ExplainerGuide(meta_data).get_explainers()

    def generate_explainer(self, request: ExplainerIdentifier) -> list[Explainer]:
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            expl_id=request, force_download=True
        )
        request.metadata = meta_data

        selected_model: Model = self._model_loader_service.load_from(request, meta_data)
        if not selected_model.is_ok():
            logger.error("empty model")
            raise Errors.MODEL_NOT_MODEL

        data: ModelData = self._data_loader_service.load(request, meta_data.data_type)
        if data and data.y_predict_is_empty():
            logger.warning(f"y_predict is empty, calculating with {meta_data.feature_names}")
            data.y_predict = selected_model.calculate_y(
                data.x_predict, 
                feature_names=meta_data.feature_names, 
                target_name=request.prediction_target
            )
            logger.info(f"Calculated y_predict: {data.y_predict}")

        results: list[ExplainerResponseData] = self._generators[
            meta_data.data_type
        ].generate(
            request=request,
            meta_data=meta_data,
            selected_model=selected_model,
            data=data,
        )

        expl_metadata = ExplainerMetaData(
            meta_data=meta_data,
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
