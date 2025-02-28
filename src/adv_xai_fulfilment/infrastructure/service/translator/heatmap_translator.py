from ....domain.model.explainers.response_data import Heatmap


class HeatmapTranslator:
    def translate(self, data: list[str]) -> Heatmap:
        obj = Heatmap()
        for d in data:
            obj.add(d)
        return obj
