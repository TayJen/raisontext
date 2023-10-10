from typing import List

from raisontext.dev.train.base import Model


class NaiveClassifier(Model):
    """Naive classifier."""

    def __str__(self):
        return "NaiveClassifier"

    def save(self, path):
        return self

    def predict(self, texts: List[str]) -> List[float]:
        pred_labels = [1 if len(text) > 100 else 0 for text in texts]
        return pred_labels
