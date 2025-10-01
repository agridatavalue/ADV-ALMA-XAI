from ..model import Model


class FdmlModel(Model):
    def __init__(self, filename: str, handler: object = None, name: str = ""):
        super().__init__(filename, handler, name)
        self.can_handle_federated = True