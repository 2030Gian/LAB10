from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import settings
from app.middleware.logging_middleware import LoggingMiddleware

Path(settings.IMAGES_DIR).mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Poke Images Service",
    description="Microservicio para consultar imágenes de Pokémon",
    version="1.0.0",
)

app.add_middleware(LoggingMiddleware)

app.mount(
    "/static/images",
    StaticFiles(directory=settings.IMAGES_DIR),
    name="pokemon-images",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "service": "PokeImages",
        "message": "Poke Images Service is running"
    }