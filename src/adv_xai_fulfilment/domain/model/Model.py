class Model:
    name: str
    handler: any
    filename: str

    def __init__(self, handler: any, name: str = "", filename: str = ""):
        self.name = name
        self.handler = handler
        self.filename = filename
