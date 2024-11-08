class Answer:
    _type: str
    _text: str
    _value: str

    def __init__(self, type: str, text: str, value: str):
        self._type = type
        self._text = text
        self._value = value

    def to_dict(self) -> dict:
        return {"type": self._type, "label": self._text, "value": self._value}

    @staticmethod
    def create_radio_answer(text: str, value: str):
        return Answer("radio", text, value)
