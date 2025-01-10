from .BuildEndpoint import buildBp
from .TargetsEndpoint import targetsBp
from .GetAllQuestionsEndpoint import questionsBp
from .ExplainerDataEndpoint import explainerDataBp
from .GetFeedbackQuestionsEndpoint import feedbackBp
from .DataSourceTypesEndpoint import dataSourceTypesBp
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
    explainerDataBp,
    dataSourceTypesBp,
    dataDistributionBp,
    featureImportanceBp,
    plotModelPerformanceBp,
    featureAverageScoresBp,
    askToExplainerEndpointBp,
    modelPerformanceMetricBp,
    featureDescriptionEndpointBp,
]
