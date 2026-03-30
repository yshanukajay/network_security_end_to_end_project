from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
from network_security.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
import sys

if __name__ == "__main__":
    try:
        logging.info("Starting the training pipeline.")

        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifacts)

        logging.info("Data ingestion completed successfully.")

        logging.info("Starting data validation.")
        
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifacts,
            data_validation_config=data_validation_config
        )
        data_validation_artifacts = data_validation.initiate_data_validation()
        print(data_validation_artifacts)

        logging.info("Data validation completed successfully.")

    except Exception as e:
        logging.error(f"Error occurred while initiating data ingestion: {str(e)}")
        raise CustomException(e, sys)
    
    
