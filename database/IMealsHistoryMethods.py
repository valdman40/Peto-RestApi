from abc import ABC, abstractmethod


class IMealsHistoryMethods(ABC):
    @abstractmethod
    def __init__(self, db):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def get_by_pet_id(self, pet_id):
        pass
