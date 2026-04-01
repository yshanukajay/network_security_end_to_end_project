from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
from network_security.entity.config_entity import (
                                        ModelTrainerConfig,
                                        TrainingPipelineConfig,
                                        DataIngestionConfig,
                                        DataValidationConfig,
                                        DataTransformationConfig
                                        )       
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
        logging.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        logging.info("Starting data validation.")
        
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifacts,
            data_validation_config=data_validation_config
        )
        data_validation_artifacts = data_validation.initiate_data_validation()
        print(data_validation_artifacts)

        logging.info("Data validation completed successfully.")
        logging.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        logging.info("Starting data transformation.")

        data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(
            data_transformation_config=data_transformation_config,
            data_validation_artifact=data_validation_artifacts
        )
        data_transformation_artifacts = data_transformation.initiate_data_transformation()
        print(data_transformation_artifacts)
        
        logging.info("Data transformation completed successfully.")
        logging.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        logging.info("Starting model training.")
        model_trainer_config=ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifacts)
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        logging.info("Model training completed successfully.")
        logging.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    except Exception as e:
        logging.error(f"Error occurred while initiating data ingestion: {str(e)}")
        raise CustomException(e, sys)
    
    
