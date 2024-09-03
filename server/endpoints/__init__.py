from .BuildEndpoint import buildBp
from .AskToExplainerEndpoint import askToExplainerEndpointBp
from .PlotFeatureImportanceEndpoint import featureImportanceBp
from .PlotModelPerformanceEndpoint import plotModelPerformanceBp
from .TabulateFeatureDescriptionEndpoint import featureDescriptionEndpointBp
from .TabulateModelPerformanceMetricEndpoint import modelPerformanceMetricBp

routes = [
    buildBp,
    featureImportanceBp,
    plotModelPerformanceBp,
    askToExplainerEndpointBp,
    modelPerformanceMetricBp,
    featureDescriptionEndpointBp,
]
