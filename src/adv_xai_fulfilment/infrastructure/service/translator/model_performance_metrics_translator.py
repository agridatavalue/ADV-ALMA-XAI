from ....domain.model.explainers.response_data import ModelPerformanceMetrics


class ModelPerformanceMetricsTranslator:
    def translate(self, data: dict) -> ModelPerformanceMetrics:
        obj = ModelPerformanceMetrics()
        for k, v in data.items():
            obj.add_metric(k, v)

        return obj
