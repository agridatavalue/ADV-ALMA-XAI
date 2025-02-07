class ModelCategory:
    REGRESSION: str = "REGRESSION"
    CLASSIFICATION: str = "CLASSIFICATION"

    @staticmethod
    def from_string(category: str) -> str:
        if not category:
            return None

        sanitized_category: str = category.lower().strip()
        if sanitized_category in ["classification"]:
            return ModelCategory.CLASSIFICATION
        if sanitized_category in ["regression"]:
            return ModelCategory.REGRESSION

        raise ValueError(f"unknown model category: {category}")
