
from abc import ABC, abstractmethod

class processor(ABC):

    def __init__(self) -> None:
        self.process()


    @abstractmethod
    def process(self, doc, update_doc):
        pass

