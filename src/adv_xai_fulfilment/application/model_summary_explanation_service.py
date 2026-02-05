import json
from string import Template

from ..domain.model.model_metadata import ModelMetaData
from ..domain.model.explainer_metadata import ExplainerMetaData
from ..domain.model.explainer_identifier import ExplainerIdentifier
from ..domain.model.explainers.response_data.model_summary import ModelSummary
from ..infrastructure.service.metadata_loader_service import MetaDataLoaderService
from ..domain.model.explainers.response_data.feature_description import FeatureDescription
from ..domain.service.feature_description_service_component import FeatureDescriptionServiceComponent

NUMBER_OF_TOP_FEATURES = 5

class ModelSummaryExplanationService:
    _metadata_loader_service: MetaDataLoaderService
    _feature_description_service_component: FeatureDescriptionServiceComponent
    
    def __init__(self):
        self._metadata_loader_service = MetaDataLoaderService()
        self._feature_description_service_component = FeatureDescriptionServiceComponent()

    def get_model_summary(
        self,
        explainer_identifier: ExplainerIdentifier,
        language: str
    ) -> ModelSummary:
        with open(f'sources/summary_templates.json', 'r') as file:
            summaries: dict = json.load(file)
            template = Template(summaries.get(language, ""))
            
        model_metadata: ModelMetaData = (
            self._metadata_loader_service.load_model_metadata(explainer_identifier)
        )
        explainer_metadata: ExplainerMetaData = self._metadata_loader_service.load_explainer_metadata(
            explainer_identifier
        )
        
        feature_descriptions: list[FeatureDescription] = self._feature_description_service_component.get_data(
            explainer_identifier
        )
        grouped_feature_descriptions = {}
        for desc in feature_descriptions:
            source_type = desc.type
            if source_type not in grouped_feature_descriptions:
                grouped_feature_descriptions[source_type] = 0
            grouped_feature_descriptions[source_type] += 1
            
        features_by_importance: list = []
        if explainer_metadata.feature_importance:
            features_by_importance: list = explainer_metadata.feature_importance.get_all_by_importance()
        
        # build text template with data
        summary = template.substitute(
            model_name=model_metadata.subject_name or "AI Model",
            theme=model_metadata.project_theme,
            n_features=len(model_metadata.feature_names),
            feature_source_types=", ".join(
                f"**{num_source_type} {source_type}**"
                for source_type, num_source_type in grouped_feature_descriptions.items()
            ),
            top_features="\n".join(
                f"{i+1}. **{feature}**"
                for i, (feature, importance) in enumerate(features_by_importance[:NUMBER_OF_TOP_FEATURES])
            ),
            other_features=", ".join(
                f"**{feature}**"
                for feature in model_metadata.feature_names[NUMBER_OF_TOP_FEATURES:]
            ),
            accuracy=f"{explainer_metadata.accuracy_metric*100:.0f}%" if explainer_metadata.accuracy_metric else "",
            precision=f"{explainer_metadata.precision_metric*100:.0f}%" if explainer_metadata.precision_metric else "",
        )
        return ModelSummary().add_explanation(summary)