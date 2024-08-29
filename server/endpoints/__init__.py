from .BuildEndpoint import buildBp
from .AskToExplainerEndpoint import askToExplainerEndpointBp
from .PlotFeatureImportanceEndpoint import featureImportanceBp

routes = [buildBp, featureImportanceBp, askToExplainerEndpointBp]
