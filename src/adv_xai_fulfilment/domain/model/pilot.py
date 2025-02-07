class Pilot:
    _id: str

    def __init__(self, id: str):
        self._id = id

    @property
    def id(self) -> str:
        return self._id

    def __repr__(self) -> str:
        return f"Pilot(id={self.id})"
