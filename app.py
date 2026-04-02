import os, sys
import certifi
import pymongo
import pandas as pd

from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
from network_security.pipelines.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from network_security.utils.main_utils.utils import load_object

from network_security.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME
from network_security.utils.ml_utils.model.estimator import NetworkModelEstimator

## Get the path to the CA bundle for SSL certificate verification
ca = certifi.where()
from dotenv import load_dotenv

## Load environment variables from the .env file
load_dotenv()

## Get the MongoDB URI from environment variables
mongo_db_uri = os.getenv("MONGO_DB_URI")
print(mongo_db_uri)

## Create a MongoDB client using the URI and CA bundle for SSL verification
client = pymongo.MongoClient(mongo_db_uri, tlsCAFile=ca)

## Access the specified database and collection
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train", tags=["train"])
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_training_pipeline()
        return Response(content="Training successful!!", media_type="text/plain")
    except Exception as e:
        raise CustomException(e, sys) from e
    
@app.post("/predict", tags=["predict"])
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_models/preprocessor.pkl")
        model = load_object("final_models/model.pkl")

        estimator = NetworkModelEstimator(preprocessor=preprocessor, model=model)
        y_pred = estimator.predict(df)
        print(y_pred)

        df['predicted_column'] = y_pred

        df.to_csv("prediction_data/output.csv", index=False)
        table_html = df.to_html(classes="table table-striped", index=False)

        return templates.TemplateResponse(
            request=request,
            name="table.html",
            context={"table_html": table_html},
        )

    except Exception as e:
        raise CustomException(e, sys) from e

if __name__ == "__main__":
    try:
        app_run(app, host="localhost", port=8000)
    except Exception as e:
        raise CustomException(e, sys) from e
