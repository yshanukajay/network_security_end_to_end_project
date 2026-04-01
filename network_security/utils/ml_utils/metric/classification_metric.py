from network_security.entity.artifacts_entity import ClassificationMetricArtifact
from network_security.exception.exception import CustomException
from sklearn.metrics import f1_score, precision_score, recall_score
import sys

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        f1 = f1_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)

        classification_metric_artifact = ClassificationMetricArtifact(
            model_f1_score=f1,
            model_precision_score=precision,
            model_recall_score=recall
        )

        return classification_metric_artifact

    except Exception as e:
        raise CustomException(e, sys)