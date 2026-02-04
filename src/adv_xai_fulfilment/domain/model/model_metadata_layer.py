class ModelMetaDataLayer:
    _type: str
    _parameters: dict
    
    @property
    def type(self) -> str:
        return self._type
    
    @type.setter
    def type(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Type must be a string")
        self._type = value
    
    @property
    def parameters(self) -> dict:
        return self._parameters or {}
    
    @parameters.setter
    def parameters(self, value: dict):
        if not isinstance(value, dict):
            raise ValueError("Parameters must be a dictionary")
        self._parameters = value
        
    @staticmethod
    def create(type: str, parameters: dict = {}) -> 'ModelMetaDataLayer':
        layer = ModelMetaDataLayer()
        layer.type = type
        layer.parameters = parameters
        return layer
    
    def __str__(self) -> str:
        return f"ModelMetaDataLayer(type={self.type}, parameters={self.parameters})"
