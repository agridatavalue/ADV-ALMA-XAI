# ADV XAI FULFILMENT

<small>version 0.0.2 of 17/12/2024</small>

## Summary

-   [Glossary](#glossary)
-   [Project Description](#10-description)
-   [Software Architecture](#20-software-architecture)
    -   [Domain-Driven-Design (DDD)](#21-domain-driven-design-ddd)
    -   [Bucket Repository (SECURESTORE)](#22-bucket-repository)
    -   [Services Description](#23-services-description)
-   [Environment](#30-environment)
    -   [Test](#31-test)
    -   [Setup](#32-setup)
    -   [Start-up](#33-startup)

## Glossary

| term    | description                                                              |
| ------- | ------------------------------------------------------------------------ |
| service | by service we mean the "xai-fulfilment" project accessible via REST API; |

## [1.0] Description

This project focuses on the development of a fulfilment system based on Explainable AI (_XAI_) techniques. The goal is to provide an interface for data management and analysis, with particular attention to the transparency and interpretability of the artificial intelligence models used.

## [2.0] Software Architecture

This project is a microservice that exposes a REST server for fulfilment management. The microservice code is written following the principles of Domain-Driven Design (DDD), ensuring a modular and easily maintainable structure.

### [2.1] Domain-Driven-Design (DDD)

For the development of this project, _Domain-Driven Design (DDD)_ was adopted, an approach to software development that emphasizes collaboration between domain experts and developers to create a software model that accurately reflects the business domain reality. The main goal of _DDD_ is to manage the complexity of software systems by dividing the domain into bounded contexts and using a ubiquitous language that is understandable to both developers and domain experts.

Key concepts of _DDD_ include:

-   **Entities**: Objects that have a distinct identity and lifecycle.
-   **Value Objects**: Objects that are defined by their attributes rather than an identity.
-   **Aggregates**: Groups of entities and value objects that are treated as a single unit.
-   **Repository**: Mechanisms for accessing aggregates.
-   **Domain Services**: Operations that do not belong to any specific entity or value object.
-   **Domain Events**: Events that represent something significant that has happened in the domain.

![Domain-Driven-Design](docs/ddd.jpg)

### [2.2] Bucket Repository

The _SECURESTORE_ server is a secure and scalable repository designed to store and manage data objects. It ensures data integrity and confidentiality through encryption and access control mechanisms. The server supports various storage backends and provides a RESTful API for seamless integration with other services.

We have a proper bucket and here there is the folder organization:

![Folder Structure](docs/folder_structure.png)

### [2.3] Services Description

#### [2.3.1] ExplainerGeneratorService

-   **generate_explainer** method:

```mermaid
sequenceDiagram
    participant Client
    participant ExplainerGeneratorService
    participant ModelLoaderService
    participant MetaDataLoaderService
    participant DataLoaderService

    Client->>ExplainerGeneratorService: Build request
    activate ExplainerGeneratorService
    ExplainerGeneratorService->>ModelLoaderService: Load model
    activate ModelLoaderService
    ModelLoaderService-->>ExplainerGeneratorService: Return Model
    deactivate ModelLoaderService
    ExplainerGeneratorService->>MetaDataLoaderService: Load model metadata
    activate MetaDataLoaderService
    MetaDataLoaderService-->>ExplainerGeneratorService: Return MetaData
    deactivate MetaDataLoaderService
    ExplainerGeneratorService->>DataLoaderService: Load data
    activate DataLoaderService
    DataLoaderService-->>ExplainerGeneratorService: Return data
    deactivate DataLoaderService
    ExplainerGeneratorService->>ExplainerGeneratorService: build explainers and relative meta data
    ExplainerGeneratorService-->>Client: Return response
    deactivate ExplainerGeneratorService

```

-   **dynamic explanation** method:

```mermaid
sequenceDiagram
    participant Client
    participant ExplainerGeneratorService
    participant ModelLoaderService

    Client->>ExplainerGeneratorService: Explanation request
    activate ExplainerGeneratorService
    ExplainerGeneratorService->>ModelLoaderService: Get model metadata
    activate ModelLoaderService
    ModelLoaderService-->>ExplainerGeneratorService: Return model metadata
    deactivate ModelLoaderService
    ExplainerGeneratorService->>ExplainerGeneratorService: Verify proper endpoints for the received model
    ExplainerGeneratorService-->>Client: Return possible endpoints
    deactivate ExplainerGeneratorService
```

#### [2.3.2] QuestionService

-   **generate_from_dict** method:

```mermaid
sequenceDiagram
    participant Client
    participant QuestionService
    participant MetaDataLoader

    Client->>QuestionService: Question list request
    activate QuestionService
    QuestionService->>MetaDataLoader: Get explainer meta data
    activate MetaDataLoader
    MetaDataLoader-->>QuestionService: Return data
    deactivate MetaDataLoader
    QuestionService->>QuestionService: Verticalize question texts
    QuestionService-->>Client: Return verticalize questions
    deactivate QuestionService
```

-   **save_partner_feedback** method:

```mermaid
sequenceDiagram
    participant Client
    participant QuestionService
    participant MetaDataLoader

    Client->>QuestionService: Question list request
    activate QuestionService
    QuestionService->>MetaDataLoader: Get explainer meta data
    activate MetaDataLoader
    MetaDataLoader-->>QuestionService: Return explainer meta data
    deactivate MetaDataLoader
    QuestionService->>QuestionService: Add feedback to explainer meta data
    QuestionService->>MetaDataLoader: Upload explainer meta data
    activate MetaDataLoader
    MetaDataLoader-->>QuestionService: Return explainer meta data
    deactivate MetaDataLoader
    QuestionService-->>Client: Return response
    deactivate QuestionService
```

## [3.0] Environment

### [3.1] Test

To run tests digit:

```bash
python -m unittest -v
```

To have a _coverage_ report digit:

```bash
python -m coverage run -m unittest | python -m coverage report
```

returns:

```bash
Name                                                                                       Stmts   Miss  Cover
--------------------------------------------------------------------------------------------------------------
src/__init__.py                                                                                0      0   100%
src/adv_xai_fulfilment/application/ExplainerGeneratorService.py                               65     41    37%
src/adv_xai_fulfilment/application/ModelPerformanceMetricService.py                           31      2    94%
src/adv_xai_fulfilment/domain/model/DataType.py                                               13      5    62%
src/adv_xai_fulfilment/domain/model/ExplainerIdentifier.py                                    25      5    80%
src/adv_xai_fulfilment/domain/model/ExplainerMetaData.py                                      44     10    77%
src/adv_xai_fulfilment/domain/model/FeatureDescription.py                                     12      1    92%
src/adv_xai_fulfilment/domain/model/Model.py                                                  19      1    95%
src/adv_xai_fulfilment/domain/model/ModelMetaData.py                                          35      4    89%
src/adv_xai_fulfilment/domain/model/Partner.py                                                 9      2    78%
src/adv_xai_fulfilment/domain/model/explainers/AleExplainer.py                                13      0   100%
src/adv_xai_fulfilment/domain/model/explainers/AnchorsExplainer.py                            11      0   100%
src/adv_xai_fulfilment/domain/model/explainers/CounterFactualsPrototypesExplainer.py          11      0   100%
src/adv_xai_fulfilment/domain/model/explainers/CounterFactualsWithRlExplainer.py              11      0   100%
src/adv_xai_fulfilment/domain/model/explainers/DataTypeModelExplainer.py                       7      0   100%
src/adv_xai_fulfilment/domain/model/explainers/DeepExplainerExplainer.py                       9      1    89%
src/adv_xai_fulfilment/domain/model/explainers/Explainer.py                                   53      8    85%
src/adv_xai_fulfilment/domain/model/explainers/IntegratedGradientsExplainer.py                11      0   100%
src/adv_xai_fulfilment/domain/model/explainers/KernelExplainerExplainer.py                    14      1    93%
src/adv_xai_fulfilment/domain/model/explainers/KernelSHAPExplainer.py                         10      0   100%
src/adv_xai_fulfilment/domain/model/explainers/PartialDependenceExplainer.py                  11      0   100%
src/adv_xai_fulfilment/domain/model/explainers/PartialDependenceVarianceExplainer.py          11      0   100%
src/adv_xai_fulfilment/domain/model/explainers/PermutationImportanceExplainer.py              11      0   100%
src/adv_xai_fulfilment/domain/model/explainers/RegressionExplainer.py                         11      2    82%
src/adv_xai_fulfilment/domain/model/explainers/SimilarityExplanationsExplainer.py             11      0   100%
src/adv_xai_fulfilment/domain/model/explainers/TreeShapInterventionalExplainer.py             11      0   100%
src/adv_xai_fulfilment/domain/model/explainers/TreeShapPathDependentExplainer.py              11      0   100%
src/adv_xai_fulfilment/domain/model/explainers/__init__.py                                    16      0   100%
src/adv_xai_fulfilment/domain/model/machineLearningModel/KerasModel.py                        15      2    87%
src/adv_xai_fulfilment/domain/model/machineLearningModel/ScikitLearnModel.py                   9      2    78%
src/adv_xai_fulfilment/domain/model/machineLearningModel/TorchModel.py                         5      0   100%
src/adv_xai_fulfilment/domain/model/questions/Answer.py                                       16      1    94%
src/adv_xai_fulfilment/domain/model/questions/Feedback.py                                     30      9    70%
src/adv_xai_fulfilment/domain/model/questions/Question.py                                     42      2    95%
src/adv_xai_fulfilment/domain/service/ExplainerRetriever.py                                   21      1    95%
src/adv_xai_fulfilment/domain/service/FeatureDescriptionServiceComponent.py                   11      2    82%
src/adv_xai_fulfilment/domain/service/FeatureImportanceServiceComponent.py                    57     27    53%
src/adv_xai_fulfilment/domain/service/ModelPerformanceServiceComponent.py                     17      1    94%
src/adv_xai_fulfilment/domain/service/ModelTranslator.py                                      20      0   100%
src/adv_xai_fulfilment/infrastructure/Constants.py                                            24      0   100%
src/adv_xai_fulfilment/infrastructure/Helper.py                                               11      0   100%
src/adv_xai_fulfilment/infrastructure/repository/BucketRepository.py                          14      6    57%
src/adv_xai_fulfilment/infrastructure/service/DataLoaderService.py                            67     22    67%
src/adv_xai_fulfilment/infrastructure/service/ExplainerRepositoryService.py                   39     21    46%
src/adv_xai_fulfilment/infrastructure/service/ModelLoaderService.py                           39      7    82%
src/adv_xai_fulfilment/infrastructure/service/translator/ExplainerMetaDataTranslator.py       18      0   100%
src/adv_xai_fulfilment/infrastructure/service/translator/ExplainerTranslator.py                4      0   100%
src/adv_xai_fulfilment/infrastructure/service/translator/FeatureDescriptionTranslator.py       4      0   100%
src/adv_xai_fulfilment/infrastructure/service/translator/FeedbackTranslator.py                13      3    77%
src/adv_xai_fulfilment/infrastructure/service/translator/ModelMetaDataTranslator.py            8      0   100%
src/adv_xai_fulfilment/presentation/translator/DataPresentationsOutputTranslator.py            6      0   100%
src/adv_xai_fulfilment/presentation/translator/ExplainerIdentifierTranslator.py                5      0   100%
src/adv_xai_fulfilment/presentation/translator/FeedbackRequestTranslator.py                   15      0   100%
tests/__init__.py                                                                             21      0   100%
--------------------------------------------------------------------------------------------------------------
TOTAL                                                                                       1449    215    85%
```

### [3.2] Setup

Programming language required:

```bash
python 3.9.0
```

Installation script:

```bash
pyenv local 3.9.0
pyenv exec python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### [3.3] Start-up

#### DEBUG mode

```bash
.\venv\Scripts\activate
python .\startServer.py -LEVEL DEBUG
```

```bash
pyenv activate xai
python .\startServer.py -LEVEL DEBUG
```

the debug server will be accessible with swagger at the endpoint `http://localhost:8505/api/doc`

push on agridatavalue gitlab
create the tag

---

Contact: <m.colageo@almaviva.it>
