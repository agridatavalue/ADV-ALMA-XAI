from ..model import Model


class FdmlModel(Model):
    @staticmethod
    def can_handle_federated() -> bool:
        return True