from .BuildEndpoint import buildBp
from .AskToExplainerEndpoint import askToExplainerEndpointBp
from .PlotFeatureImportanceEndpoint import featureImportanceBp
from .TabulateFeatureDescriptionEndpoint import featureDescriptionEndpointBp

routes = [
    buildBp,
    featureImportanceBp,
    askToExplainerEndpointBp,
    featureDescriptionEndpointBp,
]
