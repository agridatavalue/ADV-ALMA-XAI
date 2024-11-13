from ..Model import Model


class TorchModel(Model):
    @staticmethod
    def supported_frameworks() -> list[str]:
        return ["torch", "pytorch"]
