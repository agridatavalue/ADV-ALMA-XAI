import torch
import torch.nn as nn

from .fdml_model import FdmlModel
from .torch_model import TorchModel

class FdmlTorchModel(TorchModel, FdmlModel):
    def load(self, data: dict) -> "FdmlTorchModel":
        layers = []
        for layer in data.get('layers', []):
                mapped_types = {
                    "Conv1d": nn.Conv1d,
                    "ReLU": nn.ReLU,
                    "MaxPool1d": nn.MaxPool1d,
                    "Flatten": nn.Flatten,
                    "Dropout": nn.Dropout,
                    "Linear": nn.Linear,
                }
                layers.append(mapped_types[layer.type](**layer.parameters))
            
        self.handler = nn.Sequential(*layers)
        self.handler.load_state_dict(torch.load(data.get('path', '')))
        return self
    
        

