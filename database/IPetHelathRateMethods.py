from abc import ABC, abstractmethod


class IPetHelathRateMethods(ABC):
    @abstractmethod
    def __init__(self, db):
        pass

    @abstractmethod
    def put(self, pet):
        pass

    @abstractmethod
    def get_today(self, pet_id):
        pass

    @abstractmethod
    def update(self, pet_id):
        pass
