import pickle
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
    #save variable modeltype to be BB if metadata["modeltype"]=="BlackBox", WB if metadata["modeltype"]=="WhiteBox" else BBWB
    modeltype = metadata['modeltype']
    #datatype is "Tabular" if metadata["Tabular"]=="Yes", "Text" if metadata["Text"]=="Yes", "Images" if metadata["Images"]=="Yes"
    datatype = metadata['datatype']
    model_category = metadata['modelcategory']
    
    
    #we need to find the right explainer based on a dict
    
    #find the element in the dict that has same modeltype, has "Yes" in the correct flield (e.g. "Regression" if metadata["modelcategory"]=="Regression") and has "Yes" in the correct data type (e.g. "Tabular" if metadata["datatype"]=="Tabular")
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
        print("Name is RegressionExplainer and data shapes are {} and {}".format(data['x'].shape, data['y'].shape))
        explainer = func(model, data['x'], data['y']),
    elif metadata['name'] == "PartialDependence":
        explainer = func(predictor=model.predict,
                       feature_names=metadata["featurenames"],
                       categorical_names=categorical_names,
                       target_names=metadata["targetnames"]), 
    elif metadata['name'] == "PDVariance":
    
    return explainer


def train_explanator(model, metadata, data):
    """
        train_explanator

        Function that trains a explanator given the information
        provided by the metadata

        Inputs
        --------
        model: function with a .predict() method
        metadata (dict): dictionary with the input metadata

        Outputs
        ---------
        explainer: xai artifact
        metadata: complete metadata to be stored with the explainer

    """
    possible_explainers = select_explainer(metadata)
    os.makedirs('explainers', exist_ok=True)
    stored = []
    for explainer_name in possible_explainers:
        exp_metadata = {**metadata,
                    #"explainer_meta":get_model_meta(),
                    "id": 1, # TODO: Change for a unique id
                    "name":explainer_name,
                    "xplanationscope":"global",
                    "xplainerparameters":"n/a", # TODO: Change it
                    "xplanationtype":"feature_importance", # TODO: Change it
                    "xplanationmetrics":"n/a", # TODO: Change it
                    "modelparameters":"n/a", # TODO: Change it
                    "modelspecifictype":"n/a", # TODO: Change it
                    "xaidependencies":  ['numpy', 'Scikit-learn','alibi[ray]']
                    }
          # saving explainer

        # Construct the filename with the unique identifier
        filename = f'explainers/{explainer_name}.pkl'
        explainer = create_explainer(explainer_mapping[explainer_name][metadata['datatype']], model, exp_metadata, data)
         #TODO: check if this works for all explainers
        # Save the model to the pickle file
        with open(filename, 'wb') as file:
            pickle.dump(explainer, file)
        print("Stored explainer in", filename)
        json_filename = f'explainers/{explainer_name}.json'

        # Save the data to the JSON file
        
        with open(json_filename, 'w') as json_file:
            json.dump(exp_metadata, json_file, indent=2)
        print("Stored metadata in", json_filename)
        stored.append((filename, json_filename))
    return stored
