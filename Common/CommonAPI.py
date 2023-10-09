from abc import ABC, abstractmethod

class CommonAPI(ABC):
    @abstractmethod
    def ConnectAPI(self):
        pass

