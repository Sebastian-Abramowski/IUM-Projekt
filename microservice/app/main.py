from fastapi import FastAPI

from app.api.routes import prediction
from app.config.logger_config import configure_logger
from app.db.database import init_db


async def lifespan(app):
    init_db()
    configure_logger()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(prediction.router)
