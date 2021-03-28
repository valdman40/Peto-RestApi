from abc import ABC, abstractmethod


class VideoDBMethodsAbstract(ABC):
    @abstractmethod
    def __init__(self, db, model):
        pass

    @abstractmethod
    def get(self, video_id):
        pass

    @abstractmethod
    def put(self, video):
        pass
