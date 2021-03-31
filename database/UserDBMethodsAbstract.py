from abc import ABC, abstractmethod


class UserDBMethodsAbstract(ABC):
    @abstractmethod
    def __init__(self, db, model):
        pass

    @abstractmethod
    def get(self, username, password):
        pass

    @abstractmethod
    def put(self, user):
        pass

    @abstractmethod
    def update(self, user):
        pass
