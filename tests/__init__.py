# APPLICATION -----------------------------------------------------------------
from .src.application.partial_dependence_service_unittest import (
    TestPartialDependenceService,
)
from .src.application.feature_importance_service_unittest import (
    TestFeatureImportanceService,
)
# from .src.application.ExplainerGeneratorService_unittest import (
#     TestExplainerGeneratorService,
# )
from .src.application.feature_description_service_unittest import (
    TestFeatureDescriptionService,
)
from .src.application.model_performance_metric_service_unittest import (
    TestModelPerformanceMetricService,
)

# DOMAIN ----------------------------------------------------------------------
from .src.domain.model.question_unittest import TestQuestion
from .src.domain.model.model_category_unittest import TestModelCategory
from .src.domain.service.model_translator_unittest import TestModelTranslator
from .src.domain.model.explainer_meta_data_unittest import TestExplainerMetaData
from .src.domain.service.explainer_retriever_unittest import TestExplainerRetriever
from .src.domain.model.explainers.response_data.heatmap_unittest import TestHeatmap
from .src.domain.model.machineLearningModel.keras_model_unittest import TestKerasModel

# ----> SERVICE
from .src.domain.service.model_performance_service_component_unittest import (
    TestModelPerformanceServiceComponent,
)
from .src.domain.service.feature_importance_service_component_unittest import (
    TestFeatureImportanceServiceComponent,
)

# ----> EXPLAINERS
from .src.domain.model.explainers.explainer_unittest import TestExplainer
from .src.domain.model.explainers.ale_explainer_unittest import TestAleExplainer
from .src.domain.model.explainers.kernel_explainer_explainer_unittest import (
    TestKernelExplainerExplainer,
)


# INFRASTRUCTURE --------------------------------------------------------------
from .src.infrastructure.helper_unittest import TestHelper
from .src.infrastructure.service.data_loader_service_unittest import TestDataLoaderService
from .src.infrastructure.repository.bucket_repository_unittest import (
    TestBucketRepository,
)
from .src.infrastructure.service.explainer_repository_service_unittest import (
    TestExplainerRepositoryService,
)
from .src.infrastructure.service.model_loader_service_unittest import (
    ModelLoaderServiceTest,
)
from .src.infrastructure.service.translator.model_metadata_translator_unittest import (
    TestModelMetaDataTranslator,
)
from .src.infrastructure.service.translator.explainer_metadata_translator_unittest import (
    TestExplainerMetaDataTranslator,
)
from .src.infrastructure.service.translator.feature_description_translator_unittest import (
    TestFeatureDescriptionTranslator,
)
from .src.infrastructure.service.translator.feedback_translator_unittest import (
    TestFeedbackTranslator,
)

# PRESENTATION ----------------------------------------------------------------
# ----> TRANSLATORS

from .src.presentation.translator.feedback_request_translator_unittest import (
    TestFeedbackRequestTranslator,
)
from .src.presentation.translator.explainer_identifier_translator_unittest import (
    TestExplainerIdentifierTranslator,
)
from .src.presentation.translator.data_presentations_output_translator_unittest import (
    TestDataPresentationsOutputTranslator,
)
from .src.presentation.validator.explainer_generator_validator_unittest import (
    TestExplainerGeneratorValidator,
)