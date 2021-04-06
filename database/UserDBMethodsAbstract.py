from abc import ABC, abstractmethod


class UserDBMethodsAbstract(ABC):
    @abstractmethod
    def __init__(self, db, model):
        pass

    @abstractmethod
    def login(self, username, password):
        pass

    @abstractmethod
    def get_by_username(self, username):
        pass

    @abstractmethod
    def put(self, user):
        pass

    @abstractmethod
    def update(self, user):
        pass
