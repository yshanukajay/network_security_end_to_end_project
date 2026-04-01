from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import yaml
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
import os, sys
import numpy as np
#import dill
import pickle

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e, sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool=False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        raise CustomException(e, sys)
    

def save_numpy_array_data(file_path: str, array: np.array) -> None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        np.save(file_path, array)
    except Exception as e:
        raise CustomException(e, sys)
    

def load_numpy_array_data(file_path: str) -> np.array:
    try:
        if not os.path.exists(file_path):
            raise CustomException(f"The file: {file_path} does not exist", sys)
        return np.load(file_path)
    except Exception as e:
        raise CustomException(e, sys) from e
    

def save_object(file_path: str, obj: object) -> None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    

def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise CustomException(f"The file: {file_path} does not exist", sys)
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys) from e
    

def evaluate_model(X_train, y_train, X_test, y_test, models, params):
    report = {}

    try:
        logging.info(f"Evaluating models: {list(models.keys())} with hyperparameters: {params}")
        for name, model in models.items():
            gs = GridSearchCV(model, params[name], cv=3)
            gs.fit(X_train, y_train)

            best_model = gs.best_estimator_
            # Keep the fitted/tuned estimator so callers can use it directly.
            models[name] = best_model
            y_test_pred = best_model.predict(X_test)
            score = r2_score(y_test, y_test_pred)
            logging.info(f"Model: {name} has R2 score: {score} on test data")
            report[name] = score
        
        return report
    
    except Exception as e:
        logging.error(f"Error occurred while evaluating models: {e}")
        raise CustomException(e, sys)