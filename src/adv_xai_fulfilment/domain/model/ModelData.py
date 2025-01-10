import os


class ModelData:
    folder: str

    def __init__(self, folder: str):
        self.folder = folder

    def get_locale_folder_path(self, model: str) -> str:
        return os.path.join(os.getenv("TEMP"), model, self.folder)
