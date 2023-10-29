import uuid
from typing import List
from abc import ABC, abstractmethod


class Model(ABC):
    def __init__(self, descr):
        self.descr = descr
        self.hash = uuid.uuid4()

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abstractmethod
    def save(self, destination):
        raise NotImplementedError

    @abstractmethod
    def predict(self, texts: List[str]) -> List[float]:
        raise NotImplementedError