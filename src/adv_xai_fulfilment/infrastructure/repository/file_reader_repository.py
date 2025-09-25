import numpy as np
import pandas as pd

class FileReaderRepository:
    _handled_extensions_file: dict
    
    def __init__(self):
        self._handled_extensions_file = {
            'csv': self._read_csv,
            'npy': self._read_npy,
            'json': self._read_json,
            'xlsx': self._read_excel,
        }
    
    def read(self, path: str) -> pd.DataFrame:
        file_extension = path.split('.')[-1].lower()
        if file_extension not in self._handled_extensions_file:
            raise ValueError(f"File extension '{file_extension}' is not supported.")
        
        return self._handled_extensions_file.get(file_extension, self._read_csv)(path)
    
    # --------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------
    
    def _read_csv(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path)
    
    def _read_json(self, path: str) -> pd.DataFrame:
        return pd.read_json(path)
    
    def _read_excel(self, path: str) -> pd.DataFrame:
        return pd.read_excel(path)
    
    def _read_npy(self, path: str) -> pd.DataFrame:
        return np.load(path)