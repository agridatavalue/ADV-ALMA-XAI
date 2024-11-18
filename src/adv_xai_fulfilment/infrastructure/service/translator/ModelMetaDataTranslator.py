from ....domain.model.ModelMetaData import ModelMetaData
from ....domain.model.FeatureDescription import FeatureDescription

"""
{
    'partner': 'InAgro', 
    'Pilot': 'Pilot 8', 
    'Subject': 'Crop', 
    'Subjectname': 'Leek', 
    'projecttheme': 'Crop yield prediction/fertilization', 
    'modelname': 'TODO', 
    'modelid': 'TODO', 
    'framework': 'Tensorflow-Keras', 
    'algorithm': 'CNN', 
    'modelcategory': 'Regression', 
    'modeltype': 'BlackBox', 
    'datatype': 'Tabular', 
    'allfeaturenames': ['feature1', 'feature2', 'feature3'], 
    'targetnames': ['Biomass', 'N-content crop', 'N-uptake'], 
    'featurenames': ['Row distance (cm)', 'NO3-N 0-30 cm start (kg/ha)', 'NO3-N 30-60 cm start (kg/ha)', 'NO3-N 60-90 cm start (kg/ha)', 'NO3-N 0-60 cm start (kg/ha)', 'OC% (0-30 cm)', 'pH (0-30 cm)', 'EC ms/m (0-30 cm)', 'NO3-N 0-30 cm', 'NO3-N 30-60 cm', 'NO3-N 60-90 cm', 'NO3-N 0-60 cm', 'NO3-N 0-90 cm', 'orthorefl.ms.1.', 'orthorefl.ms.2.', 'orthorefl.ms.3.', 'orthorefl.ms.4.', 'orthorefl.ms.5.', 'NDVI', 'FAPAR'], 
    'feature_descriptions': {'Row distance (cm)': {'description': 'Distance between plantation rows in cm', 'source': 'field measurement', 'type': 'agronomic'}, 'NO3-N 0-30 cm start (kg/ha)': {'description': 'Nitrate content in the soil at 0-30 cm depth at the start of the season', 'source': 'agronomic', 'type': 'soil'}, 'NO3-N 30-60 cm start (kg/ha)': {'description': 'Nitrate content in the soil at 30-60 cm depth at the start of the season', 'source': 'agronomic', 'type': 'soil'}, 'NO3-N 60-90 cm start (kg/ha)': {'description': 'Nitrate content in the soil at 60-90 cm depth at the start of the season', 'source': 'agronomic', 'type': 'soil'}, 'NO3-N 0-60 cm start (kg/ha)': {'description': 'Nitrate content in the soil at 0-60 cm depth at the start of the season', 'source': 'agronomic', 'type': 'soil'}, 'OC% (0-30 cm)': {'description': 'Organic carbon content in the soil at 0-30 cm depth', 'source': 'soil scan', 'type': 'soil'}, 'pH (0-30 cm)': {'description': 'pH in the soil at 0-30 cm depth', 'source': 'soil scan', 'type': 'soil'}, 'EC ms/m (0-30 cm)': {'description': 'Electric conductivity in the soil at 0-30 cm depth', 'source': 'soil scan', 'type': 'soil'}, 'NO3-N 0-30 cm': {'description': 'Nitrate content in the soil at 0-30 cm depth', 'source': 'agronomic', 'type': 'soil'}, 'NO3-N 30-60 cm': {'description': 'Nitrate content in the soil at 30-60 cm depth', 'source': 'agronomic', 'type': 'soil'}, 'NO3-N 60-90 cm': {'description': 'Nitrate content in the soil at 60-90 cm depth', 'source': 'agronomic', 'type': 'soil'}, 'NO3-N 0-60 cm': {'description': 'Nitrate content in the soil at 0-60 cm depth', 'source': 'agronomic', 'type': 'soil'}, 'NO3-N 0-90 cm': {'description': 'Nitrate content in the soil at 0-90 cm depth', 'source': 'agronomic', 'type': 'soil'}, 'orthorefl_ms_1_': {'description': 'Orthorectified reflectance at 1st wavelength', 'source': 'remote sensing', 'type': 'spectral'}, 'orthorefl_ms_2_': {'description': 'Orthorectified reflectance at 2nd wavelength', 'source': 'remote sensing', 'type': 'spectral'}, 'orthorefl_ms_3_': {'description': 'Orthorectified reflectance at 3rd wavelength', 'source': 'remote sensing', 'type': 'spectral'}, 'orthorefl_ms_4_': {'description': 'Orthorectified reflectance at 4th wavelength', 'source': 'remote sensing', 'type': 'spectral'}, 'orthorefl_ms_5_': {'description': 'Orthorectified reflectance at 5th wavelength', 'source': 'remote sensing', 'type': 'spectral'}, 'NDVI': {'description': 'Normalized Difference Vegetation Index', 'source': 'remote sensing', 'type': 'spectral'}, 'FAPAR': {'description': 'Fraction of Absorbed Photosynthetically Active Radiation', 'source': 'remote sensing', 'type': 'spectral'}}}
"""


class ModelMetaDataTranslator:
    def translate_feature_descriptions(self, data: dict) -> list[FeatureDescription]:
        return [
            FeatureDescription(
                name=key,
                type=data[key].get("type"),
                source=data[key].get("source"),
                description=data[key].get("description"),
            )
            for key in data.keys()
        ]

    def translate(self, data: dict) -> ModelMetaData:
        return ModelMetaData(
            data_type=data.get("datatype"),
            algorithm=data.get("algorithm", "cnn"),
            framework=data.get("framework", "keras"),
            model_type=data.get("modeltype"),
            target_names=data.get("targetnames"),
            subject_name=data.get("Subjectname"),
            model_category=data.get("modelcategory"),
            feature_names=data.get("featurenames"),
            feature_descriptions=self.translate_feature_descriptions(
                data.get("feature_descriptions", {})
            ),
        )
