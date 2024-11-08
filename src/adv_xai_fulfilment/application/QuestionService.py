from src.adv_xai_fulfilment.domain.model.questions.Question import Question
from src.adv_xai_fulfilment.infrastructure.service.DataLoaderService import (
    DataLoaderService,
)


class QuestionService:
    _data_loader_service: DataLoaderService

    def __init__(self):
        self._data_loader_service = DataLoaderService()

    def generate_from_dict(self, metadata_filename: dict) -> list[Question]:
        data = None
        if metadata_filename:
            data: dict = self._data_loader_service.load_meta_data(metadata_filename)

        return [q.verticalize_for(data) for q in Question.get_all()]
