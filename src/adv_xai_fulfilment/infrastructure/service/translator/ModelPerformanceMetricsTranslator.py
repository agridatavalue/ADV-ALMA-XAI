from ....domain.model.explainers.responseData import ModelPerformanceMetrics


class ModelPerformanceMetricsTranslator:
    def translate(self, data: dict) -> ModelPerformanceMetrics:
        obj = ModelPerformanceMetrics()
        for k, v in data.items():
            obj.add_metric(k, v)

        return obj
