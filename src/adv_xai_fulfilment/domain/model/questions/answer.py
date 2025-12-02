class Answer:
    _type: str
    _text: str
    _value: str

    def __init__(self, type: str, text: str, value: str):
        self._type = type
        self._text = text
        self._value = value

    @property
    def value(self) -> str:
        return self._value
    
    @property
    def text(self) -> str:
        return self._text
    
    @property
    def type(self) -> str:
        return self._type

    def to_dict(self) -> dict:
        return {"type": self._type, "label": self._text, "value": self._value}

    @staticmethod
    def create_radio_answer(text: str, value: str):
        return Answer("radio", text, value)
    
    @staticmethod
    def create_value_answer(text: str, value: str):
        return Answer("value", text, value)
