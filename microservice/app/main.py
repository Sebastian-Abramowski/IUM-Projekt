from fastapi import FastAPI

from app.api.routes import expermient, prediction
from app.config.logger_config import configure_logger
from app.db.database import init_db
from app.exceptions.handler import register_exception_handlers


async def lifespan(app):
    init_db()
    configure_logger()
    yield


app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)
app.include_router(prediction.router)
app.include_router(expermient.router)
