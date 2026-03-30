from network_security.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
from network_security.entity.config_entity import DataValidationConfig
from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from network_security.utils.main_utils.utils import read_yaml_file
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
            self.data_ingestion_artifact = data_ingestion_artifact  
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e, sys)

