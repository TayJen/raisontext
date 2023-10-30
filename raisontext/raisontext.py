from enums import Classifier


class RaisonText:

    def __init__(self) -> None:
        pass

    def evaluate_quality(self, text: str, classifier: Classifier) -> float:
        if classifier == Classifier.NaiveClassifier:
            if len(text) > 10:
                score = 1
            elif len(text) > 5:
                score = 0.5
            else:
                score = 0
        else:
            raise NotImplementedError
        return score
