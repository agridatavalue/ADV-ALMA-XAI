import torch

from ..model import Model


class TorchModel(Model):
    def load(self, path: str) -> "TorchModel":
        self.handler = torch.load(path)
        return self

    @staticmethod
    def supported_frameworks() -> list[str]:
        return ["torch", "pytorch", "yolov8"]
