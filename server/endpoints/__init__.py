from .BuildEndpoint import buildBp
from .FeatureImportanceEndpoint import featureImportanceBp
from .AskToExplainerEndpoint import askToExplainerEndpointBp

routes = [buildBp, featureImportanceBp, askToExplainerEndpointBp]
