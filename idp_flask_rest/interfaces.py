from abc import ABC, abstractmethod

class RepositoryInterface(ABC):
    @abstractmethod
    def get_all(self, **kwargs):
        pass
    
    @abstractmethod
    def get_by_id(self, id):
        pass
    
    @abstractmethod
    def create(self, data):
        pass
    
    @abstractmethod
    def update(self, id, data):
        pass
    
    @abstractmethod
    def delete(self, id):
        pass