import warnings
warnings.filterwarnings("ignore")
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from uvicorn import run as app_run

import pandas as pd
import os, sys

from sensor.logger import logging
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.utils.main_utils import load_object
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping
from sensor.constant.application import APP_HOST, APP_PORT
from sensor.constant.training_pipeline import SAVED_MODEL_DIR


app = FastAPI()

origins = ["*"]

# Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainPipeline()

        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")

        train_pipeline.run_pipeline()
        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:

        df = pd.read_csv(file.file, na_values="na")
        

        # remove spaces in column names
        df.columns = df.columns.str.strip()
        df.fillna(0, inplace=True)

        # remove target column
        if "class" in df.columns:
            df.drop(columns=["class"], inplace=True)

        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)

        if not model_resolver.is_model_exists():
            return Response("Model is not available")

        best_model_path = model_resolver.get_best_model_path()

        model = load_object(file_path=best_model_path)

        # prediction
        y_pred = model.predict(df)

        df["predicted_column"] = y_pred

        df["predicted_column"].replace(
            TargetValueMapping().reverse_mapping(), inplace=True
        )

        return {
            "predictions": df["predicted_column"].tolist()
        }

    except Exception as e:
        return Response(f"Error Occured! {e}")



def main():
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)