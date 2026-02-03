import torch
import numpy as np
import pandas as pd
import torch.nn as nn
from collections import OrderedDict

from ..model import Model


class TorchModel(Model):
    def load(self, data: dict) -> "TorchModel":
        self.handler = torch.load(data.get('path', ''))
        
        if isinstance(self.handler, OrderedDict):
            # model state dict, need to rebuild architecture
            mapped_types = {
                "Conv1d": nn.Conv1d,
                "ReLU": nn.ReLU,
                "MaxPool1d": nn.MaxPool1d,
                "Flatten": nn.Flatten,
                "Dropout": nn.Dropout,
                "Linear": nn.Linear,
            }

            activation_map = {
                "ReLU": nn.ReLU,
                "Linear": None  # nessuna attivazione
            }
            
            layers_dict = OrderedDict()
            for i, layer in enumerate(data.get('layers', [])):
                layer_type = layer.type
                params = dict(layer.parameters)
                activation = params.pop("activation", None)
                
                if layer_type == "Linear":
                    params["in_features"] = params.pop("input_size")
                    params["out_features"] = params.pop("output_size")
                
                # Nomina i layer come nel state_dict
                layer_name = f"fc{i+1}" if layer_type == "Linear" else f"{layer_type.lower()}{i+1}"
                layers_dict[layer_name] = mapped_types[layer_type](**params)

                if activation and activation_map.get(activation):
                    act_name = f"{layer_name}_{activation.lower()}"
                    layers_dict[act_name] = activation_map[activation]()

            model_architecture = nn.Sequential(layers_dict)
            model_architecture.load_state_dict(self.handler)
            self.handler = model_architecture

        return self


    @staticmethod
    def supported_frameworks() -> list[str]:
        return ["torch", "pytorch", "yolov8"]
    
    def predict(self, X):
        with torch.no_grad():
            if isinstance(X, pd.DataFrame):
                X = X.values  # oppure X.to_numpy()
            if isinstance(X, (list, np.ndarray)):
                X = torch.tensor(X, dtype=torch.float32)
            outputs = self.handler(X)
            return outputs.detach().cpu().numpy()

        
    