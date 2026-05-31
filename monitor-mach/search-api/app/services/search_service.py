import asyncio
import time
import logging
from typing import Any

from app.clients.poke_api_client import get_pokemon_from_pokeapi
from app.clients.poke_stats_client import get_pokemon_stats
from app.clients.poke_images_client import get_pokemon_image
from app.core.logger import log_event


async def search_pokemon(pokemon_name: str) -> dict[str, Any]:
    api = "/poke/search"
    function = "search_pokemon"
    start_time = time.perf_counter()

    pokemon_name = pokemon_name.strip().lower()

    log_event(
        api=api,
        function=function,
        message=f"START pokemon={pokemon_name}",
    )

    try:
        pokeapi_data = await get_pokemon_from_pokeapi(pokemon_name)

        stats_task = get_pokemon_stats(pokemon_name)
        image_task = get_pokemon_image(pokemon_name)

        stats_data, image_data = await asyncio.gather(
            stats_task,
            image_task,
        )

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        result = {
            "name": pokeapi_data.get("name", pokemon_name),
            "pokedex_id": pokeapi_data.get("id"),
            "types": pokeapi_data.get("types", []),
            "abilities": pokeapi_data.get("abilities", []),
            "stats": stats_data,
            "image_url": image_data.get("image_url"),
        }

        log_event(
            api=api,
            function=function,
            message=(
                f"END pokemon={pokemon_name} status=200 "
                f"latency_ms={latency_ms}"
            ),
        )

        return result

    except ValueError as exc:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        log_event(
            api=api,
            function=function,
            message=(
                f"END pokemon={pokemon_name} status=404 "
                f"latency_ms={latency_ms} error={str(exc)}"
            ),
            level=logging.WARNING,
        )

        raise

    except RuntimeError as exc:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        log_event(
            api=api,
            function=function,
            message=(
                f"END pokemon={pokemon_name} status=502 "
                f"latency_ms={latency_ms} error={str(exc)}"
            ),
            level=logging.ERROR,
        )

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

        raise