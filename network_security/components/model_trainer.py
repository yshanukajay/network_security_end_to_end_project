import os, sys
import mlflow
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging

from network_security.entity.artifacts_entity import (
                                        DataTransformationArtifact,
                                        ModelTrainerArtifact,
                                        ClassificationMetricArtifact
                                        )           
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.utils.ml_utils.model.estimator import NetworkModelEstimator
from network_security.utils.main_utils.utils import (
                                        evaluate_model,
                                        save_object, 
                                        load_object, 
                                        load_numpy_array_data
                                        )
from network_security.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import r2_score

import dagshub
dagshub.init(repo_owner='YohanJay23', repo_name='network_security_end_to_end_project', mlflow=True)


class ModelTrainer:
    def __init__(
            self, 
            model_trainer_config: ModelTrainerConfig, 
            data_transformation_artifact: DataTransformationArtifact
        ):
        try:
            logging.info(f"Initializing Model Trainer class with model trainer config and data transformation artifact")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            logging.info(f"Model Trainer class initialized successfully with model trainer config and data transformation artifact")
        except Exception as e:
            logging.error(f"Error while initializing Model Trainer class: {e}")
            raise CustomException(e, sys)
        
    
    def track_mlflow(self, best_model, params, classification_artifact):
        try:
            logging.info(f"Tracking model training with mlflow")
            with mlflow.start_run(run_name="Model Training"):
                f1_score = classification_artifact.model_f1_score
                precision_score = classification_artifact.model_precision_score
                recall_score = classification_artifact.model_recall_score

                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision_score", precision_score)
                mlflow.log_metric("recall_score", recall_score)

                mlflow.log_params(params)

                mlflow.sklearn.log_model(best_model, artifact_path="model")
                logging.info(f"Model training tracked successfully with mlflow")

        except Exception as e:
            logging.error(f"Error while tracking model training with mlflow: {e}")
            raise CustomException(e, sys)
                
        
    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                "Logistic Regression": LogisticRegression(verbose=1),
                "KNN": KNeighborsClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(verbose=1),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "AdaBoost": AdaBoostClassifier()
            }

            params = {
                "Logistic Regression": {
                    'C': [0.1, 1.5, 15],
                    'solver': ['liblinear', 'lbfgs']
                },
                "KNN": {
                    'n_neighbors': [3, 8, 10],
                    'weights': ['uniform', 'distance']
                },
                "Decision Tree": {
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [None, 15, 20]
                },
                "Random Forest": {
                    'n_estimators': [50, 100, 150],
                    'max_depth': [None, 15, 20, 25],
                    'min_samples_split': [2, 6, 8],
                    'min_samples_leaf': [1, 3, 4]
                },
                "Gradient Boosting": {
                    'n_estimators': [100, 150],
                    'learning_rate': [0.01, 0.1]
                },
                "AdaBoost": {
                    'n_estimators': [50, 75, 100],
                    'learning_rate': [0.01, 0.1]
                }
            }

            model_report: dict = evaluate_model(
                                        X_train=X_train, 
                                        y_train=y_train, 
                                        X_test=X_test, 
                                        y_test=y_test,
                                        models=models, 
                                        params=params
                                    ) 
            
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]
            logging.info(f"Best model found: {best_model_name} with R2 score: {best_model_score}")
            y_train_pred = best_model.predict(X_train)
            classification_train_artifact = get_classification_score(y_true=y_train, y_pred=y_train_pred)

            ##tracking training metrics and model with mlflow
            self.track_mlflow(best_model, params[best_model_name], classification_train_artifact)

            y_test_pred = best_model.predict(X_test)
            classification_test_artifact = get_classification_score(y_true=y_test, y_pred=y_test_pred)

            ##tracking test metrics and model with mlflow
            self.track_mlflow(best_model, params[best_model_name], classification_test_artifact)

            preprocessor = load_object(file_path=self.data_transformation_artifact.preprocessor_object_file_path)
            
            model_directory = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_directory, exist_ok=True)
            
            network_model_estimator = NetworkModelEstimator(preprocessor=preprocessor, model=best_model)
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model_estimator)

            ##saving the best model to final_models folder
            save_object("final_models/model.pkl", best_model)

            logging.info(f"Trained model saved successfully to {self.model_trainer_config.trained_model_file_path}")
            
            model_trainer_artifact = ModelTrainerArtifact( 
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_artifact,
                test_metric_artifact=classification_test_artifact
            )
        
            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info(f"Initiating model training process")
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            model_trainer = self.train_model(X_train, y_train, X_test, y_test)
            return model_trainer

        except Exception as e:
            logging.error(f"Error occurred while initiating model training process: {e}")
            raise CustomException(e, sys)
        