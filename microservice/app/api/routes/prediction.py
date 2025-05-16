import uuid

import pandas as pd

from fastapi import APIRouter
from loguru import logger

from app.config.predicators import advanced_model, base_model, dummy_model
from app.schemas import GetPredictionRequest, PredictionResponse

router = APIRouter(prefix="/prediction", tags=["prediction"])


@router.get("/dummy", response_model=PredictionResponse)
def get_prediction_from_dummy_model(request: GetPredictionRequest):
    logger.info("Received request for dummy prediction")

    input_df = pd.DataFrame([request.model_dump()])
    predicted_price = dummy_model.predict(input_df)[0]

    return PredictionResponse(
        prediction_uuid=uuid.uuid4(),
        predicted_price=predicted_price,
    )


@router.get("/linear_regression", response_model=PredictionResponse)
def get_prediction_from_linear_regression_model(request: GetPredictionRequest):
    logger.info("Received request for linear regression prediction")

    input_df = pd.DataFrame([request.model_dump()])
    predicted_price = base_model.predict(input_df)[0]

    return PredictionResponse(
        prediction_uuid=uuid.uuid4(),
        predicted_price=predicted_price,
    )


@router.get("/random_forest", response_model=PredictionResponse)
def get_prediction_from_random_forest_model(request: GetPredictionRequest):
    logger.info("Received request for random forest prediction")

    input_df = pd.DataFrame([request.model_dump()])
    predicted_price = advanced_model.predict(input_df)[0]

    return PredictionResponse(
        prediction_uuid=uuid.uuid4(),
        predicted_price=predicted_price,
    )
