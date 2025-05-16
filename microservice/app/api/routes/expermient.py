from random import choice

import pandas as pd

from fastapi import APIRouter, status
from loguru import logger

from app.api.dependencies import AbRepositoryDependency
from app.config.predicators import advanced_model, base_model
from app.models import ModelName
from app.schemas import GetPredictionRequest, PredictionResponse, SetFinalPriceRequest

router = APIRouter(prefix="/experiment", tags=["experiment"])

models = {
    ModelName.LINEAR_REGRESSION: base_model,
    ModelName.RANDOM_FOREST: advanced_model,
}


@router.get("/predict", response_model=PredictionResponse)
def get_ab_prediction(request: GetPredictionRequest, ab_repository: AbRepositoryDependency):
    logger.info("Received request for ab prediction")

    selected_model = choice([ModelName.LINEAR_REGRESSION, ModelName.RANDOM_FOREST])

    input_data = request.model_dump()
    input_df = pd.DataFrame([input_data])
    predicted_price = float(models[selected_model].predict(input_df)[0])

    prediction = ab_repository.save_prediction(
        input_data=input_data,
        model_type=selected_model,
        predicted_price=predicted_price,
    )

    return PredictionResponse(
        predicted_price=predicted_price,
        prediction_uuid=prediction.uuid,
    )


@router.post("/set_final_price", status_code=status.HTTP_204_NO_CONTENT)
def set_final_price(request: SetFinalPriceRequest, ab_repository: AbRepositoryDependency):
    logger.info(f"Received request to set final price {request.final_price}")

    ab_repository.save_decision(prediction_uuid=request.prediction_uuid, final_price=request.final_price)
