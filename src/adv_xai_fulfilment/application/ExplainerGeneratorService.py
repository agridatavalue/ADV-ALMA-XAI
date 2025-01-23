import logging
from dotenv import load_dotenv

from ..domain.model.Model import Model
from ..infrastructure.Constants import Errors
from ..domain.model.ModelData import ModelData
from ..domain.model.ModelMetaData import ModelMetaData
from ..domain.model.explainers.Explainer import Explainer
from ..domain.model.FeatureImportance import FeatureImportance
from ..domain.model.ExplainerMetaData import ExplainerMetaData
from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from ..domain.service.ExplainerRetriever import ExplainerRetriever
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService
from ..infrastructure.service.MetaDataLoaderService import MetaDataLoaderService
from ..infrastructure.service.ExplainerRepositoryService import (
    ExplainerRepositoryService,
)
from ..domain.service.ModelPerformanceServiceComponent import (
    ModelPerformanceServiceComponent,
)
from ..domain.service.FeatureImportanceServiceComponent import (
    FeatureImportanceServiceComponent,
)

load_dotenv()


class ExplainerGeneratorService:
    _data_loader_service: DataLoaderService
    _explainer_retriever: ExplainerRetriever
    _model_loader_service: ModelLoaderService
    _explainer_service: ExplainerRepositoryService
    _metadata_loader_service: MetaDataLoaderService

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

    def prepare_explainer(
        self, request: ExplainerIdentifier
    ) -> list[ModelMetaData, Model, ModelData]:
        logging.debug(f"downloading meta_data {request.metadata_identifier}")
        meta_data: ModelMetaData = self._metadata_loader_service.load_model_metadata(
            expl_id=request
        )
        request.metadata = meta_data

        logging.debug(f"downloading model {request.model}")
        selected_model: Model = self._model_loader_service.load_from(
            model_file_path=request.model, meta_data=meta_data
        )
        if not selected_model.is_ok():
            logging.error("empty model")
            raise Errors.MODEL_NOT_MODEL

        logging.debug(f"downloading {request.data} data if present")
        data: ModelData = self._data_loader_service.load_data(request)

        return meta_data, selected_model, data

    def describe_explainer(self, request: ExplainerIdentifier):
        meta_data, selected_model, data = self.prepare_explainer(request)

    def generate_explainer(self, request: ExplainerIdentifier) -> list[Explainer]:
        feature_importance: FeatureImportance = self._fi_service_comp.generate_data(
            request
        )

        meta_data, selected_model, data = self.prepare_explainer(request)

        if not request.prediction_target:
            request.prediction_target = meta_data.first_target_name

        logging.debug(
            f"selecting the matching Explainers for model {selected_model.name}"
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
                f"{request.prediction_target} - creating the explainer {explainer.name}"
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
                prediction_target_index=0,
                model=selected_model,
                data=data,
            ),
            feature_importance=feature_importance,
        )
        if expl_metadata.data_are_ok:
            logging.debug("uploading the explainer metadata")
            self._metadata_loader_service.upload_explainer_metadata(
                metadata=expl_metadata, expl_id=request
            )
        else:
            logging.error("explainer metadata not ok, not uploading")

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
