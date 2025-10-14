class ModelCategory:
    REGRESSION: str = "REGRESSION"
    CLASSIFICATION: str = "CLASSIFICATION"
    OBJECT_DETECTION: str = "OBJECT_DETECTION"

    @staticmethod
    def from_string(category: str) -> str:
        if not category:
            return ''

        sanitized_category: str = category.lower().strip().replace(" ", "_")
        if sanitized_category in ["classification"]:
            return ModelCategory.CLASSIFICATION
        if sanitized_category in ["regression"]:
            return ModelCategory.REGRESSION
        if sanitized_category in ["object_detection"]:
            return ModelCategory.OBJECT_DETECTION

        raise ValueError(f"unknown model category: {category}")
    
    @staticmethod
    def is_classification(category: str) -> bool:
        return category == ModelCategory.CLASSIFICATION
    
    @staticmethod
    def is_regression(category: str) -> bool:
        return category == ModelCategory.REGRESSION
