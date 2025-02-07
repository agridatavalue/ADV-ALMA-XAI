class ExplainerResponseData:
    _corresponding_endpoint: str

    def __init__(self, endpoint: str):
        self._corresponding_endpoint = endpoint

    @property
    def corresponding_endpoint(self):
        return self._corresponding_endpoint
