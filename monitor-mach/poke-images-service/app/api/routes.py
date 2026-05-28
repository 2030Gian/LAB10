import logging
import time

from fastapi import APIRouter, HTTPException

from app.core.logger import log_event
from app.models.schemas import ImageResponse
from app.services.image_repository import find_image_by_name


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "service": "PokeImages",
        "status": "UP",
    }


@router.get(
    "/images/{pokemon_name}",
    response_model=ImageResponse,
    responses={
        404: {"description": "Pokemon image not found"},
        500: {"description": "Internal server error"},
    },
)
def get_pokemon_image(pokemon_name: str):
    api = f"/images/{pokemon_name}"
    function = "get_pokemon_image"
    start_time = time.perf_counter()

    log_event(
        api=api,
        function=function,
        message=f"START pokemon={pokemon_name}",
    )

    try:
        image = find_image_by_name(pokemon_name)

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        if image is None:
            log_event(
                api=api,
                function=function,
                message=(
                    f"END pokemon={pokemon_name} status=404 "
                    f"latency_ms={latency_ms} message=PokemonImageNotFound"
                ),
                level=logging.WARNING,
            )

            raise HTTPException(
                status_code=404,
                detail=f"Pokemon image '{pokemon_name}' not found",
            )

        log_event(
            api=api,
            function=function,
            message=(
                f"END pokemon={pokemon_name} status=200 "
                f"latency_ms={latency_ms}"
            ),
        )

        return image

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

        raise HTTPException(status_code=500, detail="Internal server error")
