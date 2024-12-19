import os
import logging
import pandas as pd
from dotenv import load_dotenv

from ..domain.model.Model import Model
from ..domain.model.ModelMetaData import ModelMetaData
from ..domain.model.explainers.Explainer import Explainer
from ..domain.model.ExplainerMetaData import ExplainerMetaData
from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from ..domain.service.ExplainerRetriever import ExplainerRetriever
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService
from ..domain.service.ModelPerformanceServiceComponent import (
    ModelPerformanceServiceComponent,
)
from ..domain.service.FeatureImportanceServiceComponent import (
    FeatureImportanceServiceComponent,
)

load_dotenv()


class ExplainerGeneratorService:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _explainer_retriever: ExplainerRetriever

    _mpm_service: ModelPerformanceServiceComponent
    _fi_service_comp: FeatureImportanceServiceComponent

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._model_loader_service = ModelLoaderService()
        self._explainer_retriever = ExplainerRetriever()
        self._fi_service_comp = FeatureImportanceServiceComponent()
        self._mpm_service = ModelPerformanceServiceComponent()

    def generate_explainer(
        self, request: ExplainerIdentifier, prediction_targets: list[str]
    ) -> list[Explainer]:
        feature_importance: dict[
            "Feature" : list[str],
            "Importance" : list[float],
            "prediction_target":str,
        ] = self._fi_service_comp.generate_data(request)

        logging.debug("downloading meta data")
        meta_data: ModelMetaData = self._data_loader_service.load_model_metadata(
            request
        )
        logging.debug("downloading model")
        selected_model: Model = self._model_loader_service.load_from(
            request.model, meta_data=meta_data
        )
        logging.debug("downloading data if present")
        data: dict[str, pd.DataFrame] = self._data_loader_service.load_data(
            folder_path=request.data, bucket_name=os.getenv("DATA_FOLDER_PATH")
        )

        if not prediction_targets:
            prediction_targets = meta_data.first_target_name

        logging.debug("selecting the matching Explainers")
        possible_explainers: list[Explainer] = self._explainer_retriever.get_by_data(
            selected_model, meta_data
        )
        logging.info(
            f"found {len(possible_explainers)} explainers: {possible_explainers}"
        )

        index = 0
        all_explainers_created: list[Explainer] = []
        for target in prediction_targets:
            created_explainers: list[Explainer] = []
            for explainer in possible_explainers:
                logging.debug(f"{target} - creating the explainer {explainer.name}")
                try:
                    explainer.build(model=selected_model, data=data)
                    self._model_loader_service.upload_explainer(
                        explainer=explainer, identifier=request
                    )
                    created_explainers.append(explainer)
                    all_explainers_created.append(explainer)
                except Exception as e:
                    logging.error(
                        f"error building the explainer {explainer.name}: {str(e)}"
                    )

            expl_metadata = ExplainerMetaData(
                meta_data=meta_data,
                target_name=target,
                possible_explainers=created_explainers,
                metrics=self._mpm_service.get_metrics(
                    prediction_target_index=index,
                    model=selected_model,
                    data=data,
                ),
                feature_importance=feature_importance,
            )
            if expl_metadata.data_are_ok:
                logging.debug("uploading the explainer metadata")
                self._data_loader_service.upload(
                    model_category=meta_data.model_category,
                    explainer_data=expl_metadata,
                    target=target,
                    model_filename=selected_model.filename,
                )
            else:
                logging.error("explainer metadata not ok, not uploading")
            index += 1

        return all_explainers_created

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
