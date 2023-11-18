import uuid
from typing import List
from abc import ABC, abstractmethod

from raisontext.dev.evaluate.metrics import classification_evaluation


class Model(ABC):
    def __init__(self, descr: str, wandb_log=True, run_name: str = ''):
        self.descr = descr
        self.hash = uuid.uuid4()
        self.wandb = wandb_log
        self.config = {'project': 'raisontext', 'name': run_name}

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abstractmethod
    def save(self, destination):
        raise NotImplementedError

    @abstractmethod
    def predict(self, texts: List[str]) -> List[float]:
        raise NotImplementedError

    def evaluate(self, texts: List[str], labels: List[bool]):
        if wandb_log:

        test_pred_probas = self.predict(texts)
        return classification_evaluation(test_pred_probas, labels)

