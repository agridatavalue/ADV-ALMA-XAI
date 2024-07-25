from .BuildEndpoint import buildBp
from .AskToExplainerEndpoint import askToExplainerEndpointBp

routes = [buildBp, askToExplainerEndpointBp]
