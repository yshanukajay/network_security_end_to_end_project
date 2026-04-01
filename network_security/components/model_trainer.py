import os, sys

from network_security.exception.exception import CustomException
from network_security.logging.logger import logging

from network_security.entity.artifacts_entity import (
                                        DataTransformationArtifact,
                                        ModelTrainerArtifact,
                                        ClassificationMetricArtifact
                                        )           
from network_security.entity.config_entity import ModelTrainerConfig

from network_security.utils.main_utils.utils import (
                                        save_object, 
                                        load_object, 
                                        load_numpy_array_data
                                        )
from network_security.utils.ml_utils.metric.classification_metric import get_classification_score


class ModelTrainer:
    def __init__(
            self, 
            model_trainer_config: ModelTrainerConfig, 
            data_transformation_artifact: DataTransformationArtifact
        ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)
        
    def train_model(self, X_train, y_train):
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            model = self.train_model(X_train, y_train)


        except Exception as e:
            raise CustomException(e, sys)
        