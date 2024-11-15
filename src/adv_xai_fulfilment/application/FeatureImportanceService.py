import os
import logging
import numpy as np
import pandas as pd

from ..domain.model.Model import Model
from ..domain.model.FeatureDescription import FeatureDescription
from ..domain.model.ExplainerIdentifier import ExplainerIdentifier
from ..domain.service.ExplainerRetriever import ExplainerRetriever
from .translator.FeatureDescriptionTranslator import FeatureDescriptionTranslator
from ..infrastructure.service.DataLoaderService import DataLoaderService
from ..infrastructure.service.ModelLoaderService import ModelLoaderService
from ..infrastructure.service.ExplainerRepositoryService import (
    ExplainerRepositoryService,
)


class FeatureImportanceService:
    _data_loader_service: DataLoaderService
    _model_loader_service: ModelLoaderService
    _explainer_retriever: ExplainerRetriever
    _explainer_repository_service: ExplainerRepositoryService
    _feature_description_translator: FeatureDescriptionTranslator

    def __init__(self):
        self._data_loader_service = DataLoaderService()
        self._explainer_retriever = ExplainerRetriever()
        self._model_loader_service = ModelLoaderService()
        self._explainer_repository_service = ExplainerRepositoryService()
        self._feature_description_translator = FeatureDescriptionTranslator()

    def get_data(
        self, expl_id: ExplainerIdentifier
    ) -> dict[
        "Feature" : list[str],
        "Importance" : list[float],
        "prediction_target":str,
    ]:
        meta_data: dict = self._data_loader_service.load_model_metadata(expl_id)
        selected_model: Model = self._model_loader_service.load_from(
            expl_id.model, meta_data=meta_data
        )

        explainer = None
        for expl in self._explainer_retriever.get_for_feature_importance():
            try:
                path: str = self._explainer_repository_service.download(
                    prediction_target=expl_id.prediction_target,
                    explainer=expl,
                    category=meta_data.get("modelcategory"),
                    model=selected_model,
                )
                expl.load(path)
                explainer = expl

            except Exception as e:
                logging.error(
                    f"Error downloading explainer: {e.message if hasattr(e, 'message') else str(e)}"
                )
                continue

        if not explainer:
            logging.error("No explainer found for feature importance")
            return {
                "Feature": [],
                "Importance": [],
                "prediction_target": expl_id.prediction_target,
            }

        logging.info(f"Explainer feature-importance: {explainer}")

        X_test = np.array(
            self._data_loader_service.load_data(
                bucket_name=os.getenv("DATA_FOLDER_PATH"), folder_path="crop2"
            )["x"]
        )

        data: pd.DataFrame = selected_model.get_feature_importance(
            feature_names=self.genarate_feature_description(expl_id),
            shap_values=explainer.get_shap_values(x_test=X_test),
        )
        return self.__prepare_data(data, expl_id.prediction_target)

    def __prepare_data(self, data: pd.DataFrame, prediction: str) -> dict:
        to_ret = {
            "Feature": data["Feature"].tolist(),
            "Importance": data["Importance"].tolist(),
            "prediction_target": prediction,
        }
        if len(to_ret["Importance"]) > 0 and isinstance(to_ret["Importance"][0], list):
            to_ret["Importance"] = [d[0] for d in to_ret["Importance"]]
        return to_ret

    def genarate_feature_description(
        self, expl_id: ExplainerIdentifier
    ) -> list[FeatureDescription]:
        meta_data: dict = self._data_loader_service.load_model_metadata(expl_id)
        features: dict = (meta_data or {}).get("feature_descriptions", {})
        return [
            self._feature_description_translator.translate(key, features[key])
            for key in features.keys()
        ]
