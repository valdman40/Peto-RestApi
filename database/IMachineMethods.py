from abc import ABC, abstractmethod


class IMachineMethods(ABC):
    @abstractmethod
    def __init__(self, db):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def update(self, id, pet_id):
        pass
