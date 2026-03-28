import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifacts_entity import DataIngestionArtifact

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URI")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config          
        except Exception as e:
            raise CustomException(e, sys) 
        
    def export_collection_as_dataframe(self):
        """
        Export MongoDB collection as a pandas dataframe
        """
        try:
            logging.info("Exporting collection data as pandas dataframe")

            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))

            logging.info("Successfully exported collection data as pandas dataframe")

            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"])

            df.replace(to_replace="na", value=np.nan, inplace=True)
            return df

        except Exception as e:
            logging.error(f"Error while exporting collection data as pandas dataframe: {e}")
            raise CustomException(e, sys)
        
        
    def export_data_into_feature_store(self, df: pd.DataFrame):
        try:
            logging.info("Exporting data into feature store")

            feature_store_dir=self.data_ingestion_config.feature_store_dir
            dir_path=os.path.dirname(feature_store_dir)
            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(feature_store_dir, index=False, header=True)

            logging.info("Successfully exported data into feature store")
            return df

        except Exception as e:
            logging.error(f"Error while exporting data into feature store: {e}")
            raise CustomException(e, sys)


    def  split_data_as_train_test(self, df: pd.DataFrame):
        try:
            logging.info("Splitting data into train and test sets")

            train_set, test_set = train_test_split(
                df, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42
            )
            logging.info("Completed splitting data into train and test sets")

            train_dir_file_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(train_dir_file_path, exist_ok=True)

            test_dir_file_path=os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(test_dir_file_path, exist_ok=True)

            logging.info("Exporting train and test data to respective file paths")

            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info("Successfully exported train and test data to respective file paths")

        except Exception as e:
            logging.error(f"Error while splitting data into train and test sets: {e}")
            raise CustomException(e, sys)
                  

    def initiate_data_ingestion(self):
        try:
            df=self.export_collection_as_dataframe()
            df=self.export_data_into_feature_store(df)
            self.split_data_as_train_test(df)

            logging.info("Creating data ingestion artifact")

            data_ingestion_artifact=DataIngestionArtifact(
                training_file_path=self.data_ingestion_config.training_file_path,
                testing_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info(f"Data ingestion artifact created: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            logging.error(f"Error while initiating data ingestion: {e}")
            raise CustomException(e, sys)
        

