from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import EntityNotFoundException


def register_exception_handlers(app):
    @app.exception_handler(EntityNotFoundException)
    async def handle_entity_not_found(_: Request, exception: EntityNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exception)},
        )
