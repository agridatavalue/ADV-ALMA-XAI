class Partner:
    _id: str

    def __init__(self, id: str):
        self._id = id

    @property
    def id(self) -> str:
        return self._id
    
    def is_equal(self, other: "Partner") -> bool:
        if not isinstance(other, Partner):
            return False
        return self.id == other.id

    def __repr__(self) -> str:
        return f"Partner(id={self.id})"
