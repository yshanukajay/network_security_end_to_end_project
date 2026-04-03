import os, sys

from network_security.components import data_transformation
from network_security.cloud.s3_syncer import S3Sync
from network_security.constants.training_pipeline import TRAINING_BUCKET_NAME
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer

from network_security.entity.config_entity import (
                                        ModelTrainerConfig,
                                        TrainingPipelineConfig,
                                        DataIngestionConfig,
                                        DataValidationConfig,
                                        DataTransformationConfig
                                        )

from network_security.entity.artifacts_entity import (
                                        DataIngestionArtifact,
                                        DataValidationArtifact,
                                        DataTransformationArtifact,
                                        ModelTrainerArtifact
                                        )

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = self.data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        
        except Exception as e:
            raise CustomException(e, sys) from e
        
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )
            data_validation_artifact = self.data_validation.initiate_data_validation()
            return data_validation_artifact
        
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_transformation = DataTransformation(
                data_transformation_config=self.data_transformation_config,
                data_validation_artifact=data_validation_artifact
            )
            data_transformation_artifact = self.data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            self.model_trainer = ModelTrainer(
                model_trainer_config=self.model_trainer_config, 
                data_transformation_artifact=data_transformation_artifact
            )
            model_trainer_artifact = self.model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def sync_artifacts_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifacts/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(local_folder=self.training_pipeline_config.artifact_dir, aws_bucket_url=aws_bucket_url)
            
            logging.info(f"Artifacts directory synced to S3 bucket: {aws_bucket_url}")

        except Exception as e:
            logging.error(f"Error syncing artifacts directory to S3: {e}")
            raise CustomException(e, sys) from e
        
    def sync_final_models_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_models/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(local_folder=self.training_pipeline_config.final_model_dir, aws_bucket_url=aws_bucket_url)

            logging.info(f"Final models directory synced to S3 bucket: {aws_bucket_url}")

        except Exception as e:
            logging.error(f"Error syncing final models directory to S3: {e}")
            raise CustomException(e, sys) from e


    def run_training_pipeline(self):
        try:         
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            self.sync_artifacts_dir_to_s3()
            self.sync_final_models_dir_to_s3()
            
            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys) from e
