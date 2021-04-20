from abc import ABC, abstractmethod


class IPetDbMethods(ABC):
    @abstractmethod
    def __init__(self, db):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def get_name_user(self, name, user_id):
        pass

    @abstractmethod
    def get_by_userid(self, user_id):
        pass

    @abstractmethod
    def put(self, pet):
        pass

    @abstractmethod
    def update_name_and_type(self, pet):
        pass
    @abstractmethod
    def update_name(self, pet):
        pass
    def update_type(self, pet):
        pass


    @abstractmethod
    def delete(self, id):
        pass
