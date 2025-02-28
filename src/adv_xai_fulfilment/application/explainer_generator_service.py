import logging
from dotenv import load_dotenv

from ..domain.model.model import Model
from ..infrastructure.constants import Errors
from ..domain.model.model_data import ModelData
from ..domain.service import ExplainerRetriever
from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainer_guide import ExplainerGuide
from ..domain.model.explainers.explainer import Explainer
from ..domain.model.explainers.response_data import Heatmap
from ..domain.model.explainer_metadata import ExplainerMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data import FeatureImportance
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..domain.model.explainers.response_data import ExplainerResponseData
from ..infrastructure.service.ModelLoaderService import ModelLoaderService
from ..domain.service.heatmap_component_service import HeatmapComponentService
from ..infrastructure.service.MetaDataLoaderService import MetaDataLoaderService
from ..domain.service.model_performance_service_component import (
    ModelPerformanceServiceComponent,
)
from ..domain.service.feature_importance_service_component import (
    FeatureImportanceServiceComponent,
)
from ..infrastructure.service.ExplainerRepositoryService import (
    ExplainerRepositoryService,
)

load_dotenv()


class ExplainerGeneratorService:
    _data_loader_service: DataLoaderService
    _explainer_retriever: ExplainerRetriever
    _model_loader_service: ModelLoaderService
    _explainer_service: ExplainerRepositoryService
    _metadata_loader_service: MetaDataLoaderService
    _heatmap_component_service = HeatmapComponentService

    _mpm_service: ModelPerformanceServiceComponent
    _fi_service_comp: FeatureImportanceServiceComponent

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._explainer_retriever = ExplainerRetriever()
        self._model_loader_service = ModelLoaderService()
        self._mpm_service = ModelPerformanceServiceComponent()
        self._metadata_loader_service = MetaDataLoaderService()
        self._fi_service_comp = FeatureImportanceServiceComponent()
        self._explainer_service = ExplainerRepositoryService()
        self._heatmap_component_service = HeatmapComponentService()

    def prepare_explainer(
        self, request: ExplainerIdentifier
    ) -> list[ModelMetaData, Model, ModelData]:
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            expl_id=request
        )
        request.metadata = meta_data

        selected_model: Model = self._model_loader_service.load_from(
            model_file_path=request.model, meta_data=meta_data
        )
        if not selected_model.is_ok():
            logging.error("empty model")
            raise Errors.MODEL_NOT_MODEL

        data: ModelData = self._data_loader_service.load(request, meta_data.data_type)

        return meta_data, selected_model, data

    def describe_explainer(
        self, request: ExplainerIdentifier
    ) -> list[ExplainerResponseData]:
        logging.debug(f"downloading meta_data {request.metadata_identifier}")
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            expl_id=request
        )
        return ExplainerGuide(meta_data).get_explainers()

    def generate_explainer(self, request: ExplainerIdentifier) -> list[Explainer]:
        # TODO: refactor this method
        logging.debug(f"generating the explainer for {str(request)}")
        feature_importance: FeatureImportance = self._fi_service_comp.generate_data(
            request
        )

        meta_data, selected_model, data = self.prepare_explainer(request)

        if not request.prediction_target:
            request.prediction_target = meta_data.first_target_name
            logging.debug(
                f"prediction target not provided, using the first target: {request.prediction_target}"
            )

        genarated_images: Heatmap = Heatmap()
        if meta_data.is_image:
            genarated_images = self._heatmap_component_service.generate_data(request)

        logging.debug(
            f"selecting the matching Explainers for model {selected_model.__class__.__name__}"
        )
        possible_explainers: list[Explainer] = self._explainer_retriever.get_by_data(
            selected_model, meta_data
        )
        logging.info(
            f"found {len(possible_explainers)} explainers: {possible_explainers}"
        )

        created_explainers: list[Explainer] = []
        for explainer in possible_explainers:
            logging.debug(
                f"creating {explainer.name} explainer for target {request.prediction_target}"
            )
            try:
                explainer.build(model=selected_model, data=data)
                self._explainer_service.upload_to(
                    explainer=explainer, identifier=request
                )
                created_explainers.append(explainer)
            except Exception as e:
                logging.error(
                    f"error building the explainer {explainer.name}: {str(e)}"
                )

        expl_metadata = ExplainerMetaData(
            meta_data=meta_data,
            target_name=request.prediction_target,
            possible_explainers=created_explainers,
            metrics=self._mpm_service.get_metrics(
                prediction_target=request.prediction_target,
                model_metadata=meta_data,
                model=selected_model,
                data=data,
            ),
            genarated_images=genarated_images,
            feature_importance=feature_importance,
        )

        logging.debug("uploading the explainer metadata")
        self._metadata_loader_service.upload_explainer_metadata(
            metadata=expl_metadata, expl_id=request
        )

        return created_explainers

    def ask_to_explainer(
        self,
        request: str,
        explainer_name: str,
        explainer_identifier: ExplainerIdentifier,
    ):
        explainer: Explainer = self._explainer_retriever.get_by_name(explainer_name)
        pilot_data = self._model_loader_service.download_for(
            pilot=explainer_identifier.pilot.id
        )
        explainer.train_with_pilot_data(pilot_data)
        return explainer.ask_to_llm(request)
