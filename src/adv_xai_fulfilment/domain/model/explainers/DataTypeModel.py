class DataTypeModel:
    TEXT: str = "TEXT"
    IMAGE: str = "IMAGE"
    TABULAR: str = "TABULAR"

    @staticmethod
    def from_string(text: str):
        if text.upper() == "TEXT":
            return DataTypeModel.TEXT
        if text.upper() == "IMAGE":
            return DataTypeModel.IMAGE
        if text.upper() == "TABULAR":
            return DataTypeModel.TABULAR
        return None
