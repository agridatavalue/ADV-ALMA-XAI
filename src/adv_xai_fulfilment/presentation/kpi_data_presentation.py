from logger import get_logger

logger = get_logger()

from .validator.kpi_data_validator import KpiDataValidator
from src.adv_xai_fulfilment.application.kpi_data_service import KpiDataService

class KpiDataPresentation:
    def __init__(self):
        self._kpi_data_service = KpiDataService()
        self._kpi_data_validator = KpiDataValidator()
        
    def get_model_feedback(self, request: dict = {}):
        logger.info(f"called get_model_feedback method with params: {request}")
        sanitized_data = self._kpi_data_validator.validate_and_sanitize_model_feedback(request)
        return self._kpi_data_service.get_model_feedback(sanitized_data)