from .BuildEndpoint import buildBp
from .AskToExplainerEndpoint import askToExplainerEndpointBp
from .PlotFeatureImportanceEndpoint import featureImportanceBp
from .TabulateFeatureDescriptionEndpoint import featureDescriptionEndpointBp
from .TabulateModelPerformanceMetricEndpoint import modelPerformanceMetricBp

routes = [
    buildBp,
    featureImportanceBp,
    askToExplainerEndpointBp,
    modelPerformanceMetricBp,
    featureDescriptionEndpointBp,
]
