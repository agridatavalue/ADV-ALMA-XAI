from .build_endpoint import buildBp
from .targets_endpoint import targetsBp
from .heatmap_endpoint import heatmapBp
from .image_viewer_endpoint import imageBp
from .lift_curve_endpoint import liftcurveBp
from .anomaly_score_endpoint import anomalyScoreBp
from .get_all_questions_endpoint import questionsBp
from .feature_impact_endpoint import featureImpactBp
from .partial_dependence_endpoint import partialDepBp
from .explainer_guide_endpoint import explainerGuideBp
from .classification_plot_endpoint import labelSizesBp
from .get_feedback_questions_endpoint import feedbackBp
from .data_source_types_endpoint import dataSourceTypesBp
from .confusion_matrix_endpoint import confusionMatrixBp
from .data_distribution_endpoint import dataDistributionBp
from .get_partner_feedback_endpoint import partnerFeedbackBp
from .feature_importance_endpoint import featureImportanceBp
from .model_performance_endpoint import plotModelPerformanceBp
from .ask_to_explainer_endpoint import askToExplainerEndpointBp
from .individual_conditional_expectations_endpoint import iceBp
from .data_features_and_average_score import dataFeaturesAvarageScoreBp
from .tabulate_feature_description_endpoint import featureDescriptionEndpointBp
from .tabulate_model_performance_metric_endpoint import modelPerformanceMetricsBp

routes = [
    iceBp,
    imageBp,
    buildBp,
    targetsBp,
    heatmapBp,
    feedbackBp,
    liftcurveBp,
    questionsBp,
    labelSizesBp,
    partialDepBp,
    anomalyScoreBp,
    featureImpactBp,
    explainerGuideBp,
    partnerFeedbackBp,
    dataSourceTypesBp,
    confusionMatrixBp,
    dataDistributionBp,
    featureImportanceBp,
    plotModelPerformanceBp,
    askToExplainerEndpointBp,
    modelPerformanceMetricsBp,
    dataFeaturesAvarageScoreBp,
    featureDescriptionEndpointBp,
]
