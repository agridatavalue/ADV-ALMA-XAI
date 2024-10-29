from .BuildEndpoint import buildBp
from .TargetsEndpoint import targetsBp
from .DataSourceEndpoint import dataSourceBp
from .AskToExplainerEndpoint import askToExplainerEndpointBp
from .DataDistributionEndpoint import dataDistributionBp
from .PlotFeatureImportanceEndpoint import featureImportanceBp
from .PlotModelPerformanceEndpoint import plotModelPerformanceBp
from .DataFeatureAverageScoresEndpoint import featureAverageScoresBp
from .TabulateFeatureDescriptionEndpoint import featureDescriptionEndpointBp
from .TabulateModelPerformanceMetricEndpoint import modelPerformanceMetricBp

routes = [
    buildBp,
    targetsBp,
    dataSourceBp,
    dataDistributionBp,
    featureImportanceBp,
    plotModelPerformanceBp,
    featureAverageScoresBp,
    askToExplainerEndpointBp,
    modelPerformanceMetricBp,
    featureDescriptionEndpointBp,
]
