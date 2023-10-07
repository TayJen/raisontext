from typing import List
from abc import ABC, abstractmethod


class Model(ABC):
    def __init__(self, path):
        self.path = path
        self.load()

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def predict(self, texts: List[str]) -> List[float]:
        raise NotImplementedError