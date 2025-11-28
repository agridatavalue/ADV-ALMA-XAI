import torch
import numpy as np

from ..model import Model


class TorchModel(Model):
    def load(self, data: dict) -> "TorchModel":
        self.handler = torch.load(data.get('path', ''))
        return self

    @staticmethod
    def supported_frameworks() -> list[str]:
        return ["torch", "pytorch", "yolov8"]
    
    def predict(self, X):
        with torch.no_grad():
            if isinstance(X, (list, np.ndarray)):
                X = torch.tensor(X, dtype=torch.float32)
            outputs = self.handler(X)
            # opzionale: outputs.numpy() se serve compatibilità sklearn
            return outputs.detach().cpu().numpy()
        
    