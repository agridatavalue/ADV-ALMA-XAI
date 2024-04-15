import pandas as pd
import sklearn
import dill as pickle
import json
import os
from datetime import datetime
from xai_methods import xai_methods_dict, explainer_mapping
def load_metadata(metadata_path:str):
    """
        load_metadata
        
        Function to load the metadata from a json file.

        Note: This function will be deprecated by a MinIO Loader     
        """ 
    print(metadata_path)
    with open(metadata_path, 'r') as json_file:
        metadata = json.load(json_file)
    print(f"Data {metadata_path} loaded successfully \u2713")
    return metadata


def load_model(model_path:str):
    """
        load_model
        
        Function to load the model from a pickle file.

        Note: This function will be deprecated by a MinIO Loader
        
        """
    
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model


def load_metadata(metadata_path:str):
    """
        load_metadata
        
        Function to load the metadata from a json file.

        Note: This function will be deprecated by a MinIO Loader     
        """
    print(metadata_path)
    with open(metadata_path, 'r') as json_file:
        metadata = json.load(json_file)
    return metadata

  
def select_explainer(metadata):
    explainers = []
    modeltype = metadata['modeltype']
    datatype = metadata['datatype']
    model_category = metadata['modelcategory']
    
    
    #we need to find the right explainer based on a dict
    
    for key, value in xai_methods_dict.items():
        if modeltype in value["modeltype"] and datatype in value["datatype"] and model_category in value['modelcategory']:
            explainers.append(key)
    return explainers
    
def create_explainer(func, model, metadata, data):
    if metadata['name'] == "ALE":
        explainer = func(model.predict,
                feature_names=metadata["featurenames"],
                target_names=metadata["targetnames"])
    elif metadata['name'] == "RegressionExplainer":
        
        descriptions = metadata.get('feature_descriptions')
        #replace each . in _ for all keys in descriptions
        if descriptions:
            for key in descriptions.keys(): descriptions[key] = descriptions[key].replace(".", "_")
        print("Name is RegressionExplainer and data shapes are {} and {}".format(data['x'].shape, data['y'].shape))
        explainer = func(model, data['x'], data['y'], descriptions=descriptions)
    #elif metadata['name'] == "PartialDependence":
        #explainer = func(predictor=model.predict,
                       #feature_names=metadata["featurenames"],
                       #categorical_names=categorical_names,
                       #target_names=metadata["targetnames"]), 
    # ... TODO: add more elifs for other explainers
    #elif metadata['name'] == "PDVariance":
    
    return explainer


def save_explainer_and_metadata(explainer, filename, exp_metadata):
    """
    Save explainer and metadata to files

    Parameters:
    explainer: xai artifact
        The explainer object to be saved
    filename: str
        The filename for storing the explainer
    exp_metadata: dict
        Metadata associated with the explainer
    """
    # Save the model to the pickle file
    with open(filename, 'wb') as file:
        pickle.dump(explainer, file)
    print("Stored explainer in", filename)

    # Construct the JSON filename
    json_filename = filename.replace('.pkl', '.json')

    # Save the metadata to the JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(exp_metadata, json_file, indent=2)
    print("Stored metadata in", json_filename)


def train_explanator(model, metadata, data):
    """
    train_explanator

    Function that trains an explanator given the information
    provided by the metadata

    Inputs
    --------
    model: function with a .predict() method
    metadata (dict): dictionary with the input metadata

    Outputs
    ---------
    stored: list of tuples containing the paths of stored explainers and metadata
    """

    possible_explainers = select_explainer(metadata)
    os.makedirs('explainers', exist_ok=True)
    stored = []

    for explainer_name in possible_explainers:
        #try:
            exp_metadata = {**metadata,
                            #"explainer_meta": get_model_meta(),
                            "id": 1,  # TODO: Change for a unique id
                            "name": explainer_name,
                            "xplanationscope": "global",
                            "xplainerparameters": "n/a",  # TODO: Change it
                            "xplanationtype": "feature_importance",  # TODO: Change it
                            "xplanationmetrics": "n/a",  # TODO: Change it
                            "modelparameters": "n/a",  # TODO: Change it
                            "modelspecifictype": "n/a",  # TODO: Change it
                            "xaidependencies": ['numpy', 'Scikit-learn', 'alibi[ray]']
                            }

            # Construct the filename with the unique identifier
            filename = f'explainers/{explainer_name}'
            explainer = create_explainer(explainer_mapping[explainer_name][metadata['datatype']], model,
                                        exp_metadata, data)
            save_explainer_and_metadata(explainer, filename + ".pkl", exp_metadata)
            stored.append((filename + ".pkl", filename + ".json"))

        #except Exception as e:
            #print(f"TRAIN_EXPLANATOR: {e}")
            #continue

    return stored
