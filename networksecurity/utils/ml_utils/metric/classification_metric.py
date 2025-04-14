from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.metrics import f1_score, precision_score, recall_score

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    """
    Calculate classification metrics: F1 score, precision, and recall.
    
    :param y_true: True labels.
    :param y_pred: Predicted labels.
    :return: Dictionary containing F1 score, precision, and recall.
    """
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_precision = precision_score(y_true, y_pred)
        model_recall = recall_score(y_true, y_pred)        
        return ClassificationMetricArtifact(
            f1_score=model_f1_score,
            precision=model_precision,
            recall=model_recall
        )
    except Exception as e:
        raise NetworkSecurityException(e) from e