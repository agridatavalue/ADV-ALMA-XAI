import json


class PersistenceRepository:

    def read(self, file_path: str) -> list[dict]:
        with open(file_path) as file:
            return json.load(file) or {}
