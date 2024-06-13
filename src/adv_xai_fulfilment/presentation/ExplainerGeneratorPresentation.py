import logging

from ..application.ExplainerGeneratorService import ExplainerGeneratorService


class ExplainerGeneratorPresentation:
    _service: ExplainerGeneratorService

    def __init__(self):
        self._service = ExplainerGeneratorService()

    def build(self, modelName: str, pilot: str, metadata: str, data: str = None):
        if not modelName and pilot and metadata:
            raise Exception("Missing required params")

        logging.info(
            f"Building Explainer with modelName: {modelName}, pilot: {pilot}",
        )
        return self._service.generate_explainer(
            pilot=pilot,
            data_filename=data,
            model_filename=modelName,
            metadata_filename=metadata,
        )
