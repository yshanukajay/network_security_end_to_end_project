import os
import sys
import pandas as pd
import numpy as np

"""
Defining common constants for training pipeline
"""

TARGET_COLUMN : str = "Result"
PIPELINE_NAME : str = "NetworkSecurityPipeline"
ARTIFACT_DIR : str = "artifacts"
FILE_NAME : str = "phishingData.csv"

TRAIN_FILE_NAME : str = "train.csv"
TEST_FILE_NAME : str = "test.csv"

SCHEMA_FILE_PATH : str = os.path.join("data_schema", "schema.yml")

SAVED_MODEL_DIR : str = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"
FINAL_MODEL_DIR : str = "final_models"

"""
Data Ingestion related constants 
"""

DATA_INGESTION_COLLECTION_NAME : str ="NetworkData"
DATA_INGESTION_DATABASE_NAME : str ="NetworkSecurity"
DATA_INGESTION_DIR_NAME : str ="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR : str = "feature_store"
DATA_INGESTION_INGESTED_DIR : str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO : float = 0.2


"""
Data validation related constants 
"""

DATA_VALIDATION_DIR_NAME : str = "data_validation"
DATA_VALIDATION_VALID_DIR : str = "valid"
DATA_VALIDATION_INVALID_DIR : str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR : str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME : str = "report.yaml"


"""
Data transformation related constants 
"""

DATA_TRANSFORMATION_DIR_NAME : str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR : str = "transformed"
DATA_TRANSFORMATION_PREPROCESSOR_OBJECT_DIR : str = "preprocessor"

##knn imputer related constants
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
    #"metric": "minkowski"
}


"""
Model Trainer related constants 
"""

MODEL_TRAINER_DIR_NAME : str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR : str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME : str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE : float = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD : float = 0.05


TRAINING_BUCKET_NAME : str = "network-security-s3-test"