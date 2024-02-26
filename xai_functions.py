import pickle
import json
import os
from datetime import datetime
from alibi.explainers import ALE, PartialDependence, PDVariance, PermutationImportance, Anchors, CEM, Counterfactuals

def load_metadata(metadata_path:str):
    """
        load_metadata
        
        Function to load the metadata from a json file.

        Note: This function will be deprecated by a MinIO Loader     
        """ 
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
    with open(metadata_path, 'r') as json_file:
        metadata = json.load(json_file)
    return metadata

  
def select_explainer(model, metadata):
    explainers = []
    #save variable modeltype to be BB if metadata["modeltype"]=="BlackBox", WB if metadata["modeltype"]=="WhiteBox" else BBWB
    modeltype = "BB" if metadata["modeltype"]=="BlackBox" else "WB" if metadata["modeltype"]=="WhiteBox" else "BBWB"
    #datatype is "Tabular" if metadata["Tabular"]=="Yes", "Text" if metadata["Text"]=="Yes", "Images" if metadata["Images"]=="Yes"
    datatype = "Images" if metadata["Images"]=="Yes" else "Text" if metadata["Text"]=="Yes" else "Tabular"
    model_category = "Regression" if metadata["Regression"]=="Yes" else "Classification"
    
    
    #we need to find the right explainer based on a dict
    from xai_delivery.xai_methods import xai_methods_dict
    #find the element in the dict that has same modeltype, has "Yes" in the correct flield (e.g. "Regression" if metadata["modelcategory"]=="Regression") and has "Yes" in the correct data type (e.g. "Tabular" if metadata["datatype"]=="Tabular")
    for key, value in xai_methods_dict.items():
        if value["modeltype"]==modeltype and value["datatype"]==datatype and value['modelcategory']==model_category:
            explainers.append(key)
    return explainers
    
    
  

def train_explanator(model, metadata):
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

    explainer_mapping = {"ALE":ALE, "PartialDependence":PartialDependence, "PDVariance":PDVariance, "PermutationImportance":PermutationImportance, "Anchors":Anchors, "CEM":CEM, "Counterfactuals":Counterfactuals}
    #explainer = ALE(model.predict,
                    #feature_names=metadata["featurenames"],
                    #target_names=metadata["targetnames"])
    #explainer = select_explainer(model, metadata)
    #def get_model_meta():
        #return explainer
    possible_explainers = select_explainer(model, metadata)
    metadata = {**metadata,
                #"explainer_meta":get_model_meta(),
                "id": 1, # TODO: Change for a unique id
                "name":possible_explainers,
                "xplanationscope":"global",
                "xplainerparameters":"n/a", # TODO: Change it
                "xplanationtype":"feature_importance", # TODO: Change it
                "xplanationmetrics":"n/a", # TODO: Change it
                "modelparameters":"n/a", # TODO: Change it
                "modelspecifictype":"n/a", # TODO: Change it
                "xaidependencies":  ['numpy', 'Scikit-learn','alibi[ray]']
                }
          # saving explainer
    # Generate a unique identifier based on date and time
    current_datetime = datetime.now()
    unique_id = current_datetime.strftime("%Y%m%d_%H%M")

    # Construct the filename with the unique identifier
    os.makedirs('explainers', exist_ok=True)
    filename = f'explainers/xai_explainer_{unique_id}.pkl'

    for explainer_name in possible_explainers:
        explainer = explainer_mapping[explainer_name](model.predict,
                    feature_names=metadata["featurenames"],
                    target_names=metadata["targetnames"])
        # Save the model to the pickle file
        with open(filename, 'wb') as file:
            pickle.dump(explainer, file)
        
        json_filename = f'explainers/xai_metadata_{explainer_name}_{unique_id}.json'

    # Save the data to the JSON file
    
    with open(json_filename, 'w') as json_file:
        json.dump(metadata, json_file, indent=2)  
    
    return filename, json_filename
    #return explainer, metadata
