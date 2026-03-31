import os, sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constants.training_pipeline import TARGET_COLUMN
from network_security.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_security.entity.artifacts_entity import DataTransformationArtifact, DataValidationArtifact

from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(
            self, 
            data_transformation_config: DataTransformationConfig, 
            data_validation_artifact: DataValidationArtifact
        ):    
        try:
            self.data_transformation_config: DataTransformationConfig = data_transformation_config
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys)
        
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            logging.info(f"Reading data from file: {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(f"Error while reading data from file: {file_path}, error: {e}")
            raise CustomException(e, sys)
        
    
    def get_data_transformer_object(cls) -> Pipeline:
        try:
            logging.info("Creating data transformer object")
            KNNImputer_object: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor: Pipeline = Pipeline([
                ("imputer", KNNImputer_object)
            ])
            return preprocessor

        except Exception as e:
            logging.error(f"Error while creating data transformer object: {e}")
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")

            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            logging.info("Data read completed successfully.")

            logging.info("Splitting input and target features from both train and test dataframes.")

            input_features_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            logging.info("Target feature for training data replaced successfully.")

            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            logging.info("Target feature for test data replaced successfully.")
            logging.info("Input and target features split successfully.")

            logging.info("Applying data transformation on both train and test data.")

            preprocessor = self.get_data_transformer_object()
            preprocessor_obj = preprocessor.fit(input_features_train_df)
            input_feature_train_df_transformed = preprocessor_obj.transform(input_features_train_df)
            input_feature_test_df_transformed = preprocessor_obj.transform(input_feature_test_df)

            logging.info("Data transformation applied successfully on both train and test data.")
            logging.info("Concatenating input and target features for train and test data.")

            ## concatenate input and target features for train and test data using 'c_'function of numpy
            train_arr = np.c_[input_feature_train_df_transformed, target_feature_train_df.to_numpy()]
            test_arr = np.c_[input_feature_test_df_transformed, target_feature_test_df.to_numpy()]

            logging.info("Concatenation of input and target features for train and test data completed successfully.")
            logging.info("Saving transformed data and preprocessor object.")

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_obj)

            logging.info("Transformed data and preprocessor object saved successfully.")
            logging.info("Creating data transformation artifact.")

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path,
                preprocessor_object_file_path = self.data_transformation_config.transformed_object_file_path
            )
            
            logging.info(f"Data transformation artifact created successfully: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            logging.error(f"Error while initiating data transformation: {e}")
            raise CustomException(e, sys)