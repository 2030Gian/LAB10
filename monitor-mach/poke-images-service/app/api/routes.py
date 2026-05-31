import time
import logging
from urllib.parse import quote

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.core.logger import log_event
from app.models.schemas import PokemonImageResponse
from app.services.image_repository import (
    find_image_by_pokemon_name,
    get_relative_image_path,
)

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "service": "PokeImages",
        "status": "UP"
    }


@router.get(
    "/images/{pokemon_name}",
    response_model=PokemonImageResponse,
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
        image_path = find_image_by_pokemon_name(pokemon_name)
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        if image_path is None:
            log_event(
                api=api,
                function=function,
                message=(
                    f"END pokemon={pokemon_name} status=404 "
                    f"latency_ms={latency_ms} message=ImageNotFound"
                ),
                level=logging.WARNING,
            )

            raise HTTPException(
                status_code=404,
                detail=f"Image for Pokemon '{pokemon_name}' not found"
            )

        relative_path = get_relative_image_path(image_path)
        encoded_relative_path = quote(relative_path)

        public_base_url = settings.PUBLIC_BASE_URL.rstrip("/")
        image_url = f"{public_base_url}/static/images/{encoded_relative_path}"

        log_event(
            api=api,
            function=function,
            message=(
                f"END pokemon={pokemon_name} status=200 "
                f"latency_ms={latency_ms} image_path={relative_path}"
            ),
        )

        return {
            "name": pokemon_name,
            "image_url": image_url,
            "relative_path": f"/static/images/{encoded_relative_path}",
        }

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