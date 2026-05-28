from fastapi import FastAPI
from app.api.routes import router
from app.middleware.logging_middleware import LoggingMiddleware

app = FastAPI(
    title="Poke Stats Service",
    description="Microservicio para consultar estadísticas de Pokémon",
    version="1.0.0",
)

app.add_middleware(LoggingMiddleware)

app.include_router(router)


@app.get("/")
def root():
    return {
        "service": "PokeStats",
        "message": "Poke Stats Service is running"
    }