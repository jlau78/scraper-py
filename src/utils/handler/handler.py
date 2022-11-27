from abc import ABC, abstractmethod

class handler(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def handle(self, elements, page_config):
        pass
