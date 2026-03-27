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
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.read_csv(list(collection.find()))

            if "_id" in df.columns.to_list():
                df=df.drop(columns="_id", axis=1)

            df.replace(to_replace="na", value=np.NAN, inplace=True)
            return df

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self):
        try:
            df=self.export_collection_as_dataframe()
        except Exception as e:
            raise CustomException(e, sys)
        

