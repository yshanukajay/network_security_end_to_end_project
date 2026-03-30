import yaml
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
import os, sys
import numpy as np
#import dill
import pickle

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e, sys)