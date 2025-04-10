from abc import ABC, abstractmethod

class Domain(ABC):
    @abstractmethod
    def parse(self, response):
        pass

    @abstractmethod
    def parse_detail(self, response):
        pass
