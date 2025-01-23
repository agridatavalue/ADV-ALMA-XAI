from .BuildEndpoint import buildBp
from .TargetsEndpoint import targetsBp
from .PrepareEndpoint import prepareBp
from .GetAllQuestionsEndpoint import questionsBp
from .ExplaineGuideEndpoint import explainerGuideBp
from .PartialDependenceEndpoint import partialDepBp
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
    prepareBp,
    feedbackBp,
    questionsBp,
    partialDepBp,
    explainerGuideBp,
    dataSourceTypesBp,
    dataDistributionBp,
    featureImportanceBp,
    plotModelPerformanceBp,
    featureAverageScoresBp,
    askToExplainerEndpointBp,
    modelPerformanceMetricBp,
    featureDescriptionEndpointBp,
]
