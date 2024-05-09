class Model:
    name: str
    handler: any

    def __init__(self, name: str, handler: any):
        self.name = name
        self.handler = handler
