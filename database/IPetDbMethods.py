from abc import ABC, abstractmethod


class IPetDbMethods(ABC):
    @abstractmethod
    def __init__(self, db, model):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def get_name_user(self, name, user_id):
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
