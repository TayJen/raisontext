import uuid
from typing import List
from abc import ABC, abstractmethod

from raisontext.dev.evaluate.metrics import classification_evaluation

# import wandb

class Model(ABC):
    def __init__(self, descr: str, wandb_log=True, run_name: str = ''):
        self.descr = descr
        self.hash = uuid.uuid4()
        self.wandb = wandb_log
        if self.wandb:
            pass
            # self.wandb_run = wandb.init(project='raisontext', name=run_name)

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
        if self.wandb:
            # run = wandb.init(project='raisontext', id=self.wandb_run.id, resume='allow')
            pass

        test_pred_probas = self.predict(texts)
        metrics = classification_evaluation(test_pred_probas, labels)
        metrics.update({'test_size': len(texts)})

        if self.wandb:
            # wandb.log(metrics)
            # run.finish()
            pass

        return test_pred_probas, metrics

if __name__ == '__main__':
    print('Running classification')
