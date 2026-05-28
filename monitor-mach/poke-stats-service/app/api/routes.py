import time
import logging
from fastapi import APIRouter, HTTPException
from app.db.repository import find_pokemon_stats_by_name
from app.models.schemas import PokemonStatsResponse
from app.core.logger import log_event

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "service": "PokeStats",
        "status": "UP"
    }


@router.get(
    "/stats/{pokemon_name}",
    response_model=PokemonStatsResponse,
    responses={
        404: {"description": "Pokemon not found"},
        500: {"description": "Internal server error"},
    },
)
def get_pokemon_stats(pokemon_name: str):
    api = f"/stats/{pokemon_name}"
    function = "get_pokemon_stats"
    start_time = time.perf_counter()

    log_event(
        api=api,
        function=function,
        message=f"START pokemon={pokemon_name}",
    )

    try:
        stats = find_pokemon_stats_by_name(pokemon_name)

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        if stats is None:
            log_event(
                api=api,
                function=function,
                message=(
                    f"END pokemon={pokemon_name} status=404 "
                    f"latency_ms={latency_ms} message=PokemonNotFound"
                ),
                level=logging.WARNING,
            )

            raise HTTPException(
                status_code=404,
                detail=f"Pokemon '{pokemon_name}' not found"
            )

        log_event(
            api=api,
            function=function,
            message=(
                f"END pokemon={pokemon_name} status=200 "
                f"latency_ms={latency_ms}"
            ),
        )

        return stats

    except HTTPException:
        raise

    except Exception as exc:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        log_event(
            api=api,
            function=function,
            message=(
                f"END pokemon={pokemon_name} status=500 "
                f"latency_ms={latency_ms} error={str(exc)}"
            ),
            level=logging.ERROR,
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )