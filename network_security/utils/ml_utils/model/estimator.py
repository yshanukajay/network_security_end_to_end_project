from network_security.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
import sys

from network_security.exception.exception import CustomException
from network_security.logging.logger import logging

class NetworkModelEstimator:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise CustomException(e, sys)
    def predict(self, X):
        try:
            X_transform = self.preprocessor.transform(X)
            y_hat = self.model.predict(X_transform)
            return y_hat
        except Exception as e:
            raise CustomException(e, sys)