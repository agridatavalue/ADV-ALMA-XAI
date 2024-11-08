from .BuildEndpoint import buildBp
from .TargetsEndpoint import targetsBp
from .DataSourceEndpoint import dataSourceBp
from .GetAllQuestionsEndpoint import questionsBp
from .GetFeedbackQuestionsEndpoint import feedbackBp
from .DataDistributionEndpoint import dataDistributionBp
from .AskToExplainerEndpoint import askToExplainerEndpointBp
from .PlotFeatureImportanceEndpoint import featureImportanceBp
from .PlotModelPerformanceEndpoint import plotModelPerformanceBp
from .DataFeatureAverageScoresEndpoint import featureAverageScoresBp
from .TabulateFeatureDescriptionEndpoint import featureDescriptionEndpointBp
from .TabulateModelPerformanceMetricEndpoint import modelPerformanceMetricBp

routes = [
    buildBp,
    targetsBp,
    feedbackBp,
    questionsBp,
    dataSourceBp,
    dataDistributionBp,
    featureImportanceBp,
    plotModelPerformanceBp,
    featureAverageScoresBp,
    askToExplainerEndpointBp,
    modelPerformanceMetricBp,
    featureDescriptionEndpointBp,
]
