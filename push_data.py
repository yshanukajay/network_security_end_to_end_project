import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from dotenv import load_dotenv
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging

load_dotenv()

MONGO_DB_URI=os.getenv("MONGO_DB_URI")
print(MONGO_DB_URI)

ca=certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)

    def csv_to_json_converter(self, file_path):
        try:
            logging.info(f"Reading data from file: {file_path}")

            data=pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records=list(json.loads(data.T.to_json()).values())

            logging.info(f"Converted data to JSON format with {len(records)} records")

            return records
        
        except Exception as e:
            logging.error(f"Error occurred while converting CSV to JSON: {e}")

            raise CustomException(e,sys)
        

    def push_data_to_mongodb(self, records, database, collection_name):
        try:            
            logging.info(f"Pushing data to MongoDB database: {database}, collection: {collection_name}")
            self.database=database
            self.collection_name=collection_name
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URI)
            self.database=self.mongo_client[self.database]

            self.collection=self.database[self.collection_name]
            self.collection.insert_many(self.records)
            logging.info(f"Successfully inserted {len(self.records)} records into MongoDB collection: {collection_name}")
            return (len(self.records))
        
        except Exception as e:
            logging.error(f"Error occurred while pushing data to MongoDB: {e}")
            raise CustomException(e, sys)

if __name__=="__main__":
    try:
        logging.info("Starting the data extraction and loading process")

        FILE_PATH="network_data\phisingData.csv"
        DATABASE="NetworkSecurity"
        COLLECTION_NAME="NetworkData"

        data_extractor=NetworkDataExtract()
        records=data_extractor.csv_to_json_converter(FILE_PATH)
        no_of_records=data_extractor.push_data_to_mongodb(records, DATABASE, COLLECTION_NAME)

        logging.info(f"Data extraction and loading process completed successfully with {no_of_records} records inserted into MongoDB")
    
    except Exception as e:
        logging.error(f"An error occurred during the data extraction and loading process: {e}")

        raise CustomException(e, sys)
             

