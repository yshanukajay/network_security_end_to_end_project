from network_security.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
from network_security.entity.config_entity import DataValidationConfig
from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from network_security.utils.main_utils.utils import *
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os, sys

class DataValidation:
    def __init__(
            self, data_ingestion_artifact: DataIngestionArtifact,
            data_validation_config: DataValidationConfig
        ):
        try:
            logging.info(f"Initializing Data Validation class with data ingestion artifact and data validation config")
            
            self.data_ingestion_artifact=data_ingestion_artifact  
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)

            logging.info(f"Data Validation class initialized successfully with data ingestion artifact and data validation config")

        except Exception as e:
            logging.error(f"Error while initializing Data Validation class: {e}")
            raise CustomException(e, sys)
        
        
    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            logging.info(f"Reading data from file: {file_path}")
            return pd.read_csv(file_path)
        
        except Exception as e:
            logging.error(f"Error while reading data from file: {file_path}, error: {e}")
            raise CustomException(e, sys)
        

    def validate_no_of_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            logging.info(f"Validating number of columns in the dataframe")
            no_of_columns=len(self.schema_config["columns"])
            logging.info(f"Expected number of columns: {no_of_columns}, Found: {dataframe.shape[1]}")
            
            if no_of_columns == dataframe.shape[1]:
                logging.info(f"Number of columns in the dataframe is as expected")
                return True
            return False   
          
        except Exception as e:
            logging.error(f"Error while validating number of columns in the dataframe: {e}")
            raise CustomException(e, sys)
        

    def detect_data_drift(
            self, base_df:pd.DataFrame, current_df:pd.DataFrame, threshold:float=0.05
    ) -> bool:
        try:
            logging.info(f"Detecting data drift between base and current dataframe")
            status=False
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                ks_result =ks_2samp(d1, d2)
                if threshold <= ks_result .pvalue:
                    is_found=False
                    logging.info(f"No data drift detected in column: {column}")
                else:
                    is_found=True
                    status=True
                    logging.info(f"Data drift detected in column: {column}")

                report.update({column: {
                    "p_value": float(ks_result .pvalue),
                    "drift_status": is_found
                }})

            logging.info(f"Writing data drift report to yaml file: {self.data_validation_config.drift_report_file_path}")
            
            drift_report_file_path=self.data_validation_config.drift_report_file_path

            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)

            write_yaml_file(
                file_path=drift_report_file_path,
                content=report,
                replace=True
            )

            logging.info(f"Data drift report written to yaml file successfully")
            return status

        except Exception as e:
            logging.error(f"Error while detecting data drift: {e}")
            raise CustomException(e, sys)

        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.training_file_path
            test_file_path=self.data_ingestion_artifact.testing_file_path

            train_df=DataValidation.read_data(train_file_path)
            test_df=DataValidation.read_data(test_file_path) 

            is_train_valid=self.validate_no_of_columns(train_df)
            if not is_train_valid:
                logging.info(f"Training data is not valid")

            is_test_valid=self.validate_no_of_columns(test_df)
            if not is_test_valid:
                logging.info(f"Testing data is not valid") 
            
            logging.info("Training and testing data are valid in terms of number of columns. Proceeding to detect data drift.")

            status=self.detect_data_drift(base_df=train_df, current_df=test_df)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Saving valid training and testing data to valid directory")

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
            
            logging.info(f"Valid training and testing data saved to valid directory successfully")

            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info(f"Data validation artifact created successfully with validation status: {status}")
            logging.info(f"Valid train file path: {self.data_validation_config.valid_train_file_path}")
            logging.info(f"Valid test file path: {self.data_validation_config.valid_test_file_path}")
            logging.info(f"Drift report file path: {self.data_validation_config.drift_report_file_path}")

            return data_validation_artifact

        except Exception as e:
            logging.error(f"Error while initiating data validation: {e}")
            raise CustomException(e, sys)
        
 

