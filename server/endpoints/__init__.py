from .BuildEndpoint import buildBp
from .TargetsEndpoint import targetsBp
from .PrepareEndpoint import prepareBp
from .HeatmapEndpoint import heatmapBp
from .ImageViewerEndpoint import imageBp
from .GetAllQuestionsEndpoint import questionsBp
from .ExplaineGuideEndpoint import explainerGuideBp
from .PartialDependenceEndpoint import partialDepBp
from .GetFeedbackQuestionsEndpoint import feedbackBp
from .DataSourceTypesEndpoint import dataSourceTypesBp
from .ConfusionMatrixEndpoint import confusionMatrixBp
from .DataDistributionEndpoint import dataDistributionBp
from .AskToExplainerEndpoint import askToExplainerEndpointBp
from .PlotFeatureImportanceEndpoint import featureImportanceBp
from .PlotModelPerformanceEndpoint import plotModelPerformanceBp
from .DataFeatureAverageScoresEndpoint import featureAverageScoresBp
from .TabulateFeatureDescriptionEndpoint import featureDescriptionEndpointBp
from .TabulateModelPerformanceMetricEndpoint import modelPerformanceMetricsBp

routes = [
    imageBp,
    buildBp,
    targetsBp,
    prepareBp,
    heatmapBp,
    feedbackBp,
    questionsBp,
    partialDepBp,
    explainerGuideBp,
    dataSourceTypesBp,
    confusionMatrixBp,
    dataDistributionBp,
    featureImportanceBp,
    plotModelPerformanceBp,
    featureAverageScoresBp,
    askToExplainerEndpointBp,
    modelPerformanceMetricsBp,
    featureDescriptionEndpointBp,
]
