from fastapi import FastAPI
from app.api.routes import router
from app.middleware.logging_middleware import LoggingMiddleware

app = FastAPI(
    title="Search API",
    description="API orquestadora para buscar información completa de un Pokémon",
    version="1.0.0",
)

app.add_middleware(LoggingMiddleware)

app.include_router(router)


@app.get("/")
def root():
    return {
        "service": "SearchAPI",
        "message": "Search API is running"
    }