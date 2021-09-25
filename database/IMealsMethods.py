from abc import ABC, abstractmethod


class IMealsMethods(ABC):
    @abstractmethod
    def __init__(self, db):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def get_by_pet_id(self, pet_id):
        pass

    @abstractmethod
    def put(self, pet):
        pass

    @abstractmethod
    def update(self, pet):
        pass


    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def insertPostMeal(self, pet_id, meal):
        pass
