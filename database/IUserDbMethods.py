from abc import ABC, abstractmethod


class IUserDbMethods(ABC):
    @abstractmethod
    def __init__(self, db):
        pass

    @abstractmethod
    def login(self, username, password):
        pass

    @abstractmethod
    def put(self, user):
        pass

    @abstractmethod
    def update(self, user):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def get_by_username(self, username):
        pass

    @abstractmethod
    def update_token(self, token, id):
        pass
