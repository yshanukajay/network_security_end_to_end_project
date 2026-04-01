from network_security.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
import sys

from network_security.exception.exception import CustomException
from network_security.logging.logger import logging

class NetworkModelEstimator:
    def __init__(self, preprocessor, model):
        try:
            logging.info(f"Initializing NetworkModelEstimator class with preprocessor and model")
            self.preprocessor = preprocessor
            self.model = model
            logging.info(f"NetworkModelEstimator class initialized successfully with preprocessor and model")
            
        except Exception as e: 
            logging.error(f"Error while initializing NetworkModelEstimator class: {e}")
            raise CustomException(e, sys)
    def predict(self, X):
        try:
            logging.info(f"Making predictions with the network model")
            X_transform = self.preprocessor.transform(X)
            y_hat = self.model.predict(X_transform)
            logging.info(f"Predictions made successfully")
            return y_hat
        
        except Exception as e:
            logging.error(f"Error while making predictions with the network model: {e}")
            raise CustomException(e, sys)