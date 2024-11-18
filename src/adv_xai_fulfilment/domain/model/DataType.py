class DataType:
    TEXT: str = "TEXT"
    IMAGE: str = "IMAGE"
    TABULAR: str = "TABULAR"

    @staticmethod
    def from_string(text: str):
        if text.upper() == "TEXT":
            return DataType.TEXT
        if text.upper() == "IMAGE":
            return DataType.IMAGE
        if text.upper() == "TABULAR":
            return DataType.TABULAR
        return None
