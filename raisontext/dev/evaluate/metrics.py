from typing import List

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, \
    average_precision_score


def classification_evaluation(pred_probas: List[float], truth_labels: List[bool], threshold=0.5):
    if len(pred_probas) != len(truth_labels):
        raise ValueError("Length of predictions and truth_labels should be the same")

    # Convert predictions to binary
    binary_preds = [1 if prob >= threshold else 0 for prob in pred_probas]
    accuracy = accuracy_score(truth_labels, binary_preds)
    precision = precision_score(truth_labels, binary_preds)
    recall = recall_score(truth_labels, binary_preds)
    f1 = f1_score(truth_labels, binary_preds)

    roc_auc = roc_auc_score(truth_labels, pred_probas)
    prc_auc = average_precision_score(truth_labels, pred_probas)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc,
        "prc_auc": prc_auc
    }