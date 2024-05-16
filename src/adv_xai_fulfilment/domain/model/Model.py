class Model:
    name: str
    handler: any

    def __init__(self, handler: any, name: str = None):
        self.name = name
        self.handler = handler
