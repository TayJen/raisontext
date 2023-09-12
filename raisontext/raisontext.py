from enums import Classifier


class RaisonText:

    def __init__(self) -> None:
        pass

    def evaluate_quality(text: str, classifier: Classifier) -> float:
        if classifier == Classifier.NaiveClassifier:
            if len(text) > 100:
                score = 1
            else:
                score = 0
        else:
            raise NotImplementedError
        return score
