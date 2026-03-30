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

SCHEMA_FILE_PATH : str = os.path.join("data_schema", "schema.yaml")

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



