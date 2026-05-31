import time
import logging
from typing import Any
import httpx

from app.core.config import settings
from app.core.logger import log_event


async def get_pokemon_stats(pokemon_name: str) -> dict[str, Any]:
    api = f"/stats/{pokemon_name}"
    function = "get_pokemon_stats"
    start_time = time.perf_counter()

    pokemon_name = pokemon_name.strip().lower()
    url = f"{settings.POKE_STATS_BASE_URL.rstrip('/')}/stats/{pokemon_name}"

    log_event(
        api=api,
        function=function,
        message=f"START pokemon={pokemon_name} url={url}",
    )

    try:
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECONDS) as client:
            response = await client.get(url)

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        if response.status_code == 404:
            log_event(
                api=api,
                function=function,
                message=(
                    f"END pokemon={pokemon_name} status=404 "
                    f"latency_ms={latency_ms} message=StatsNotFound"
                ),
                level=logging.WARNING,
            )

            raise ValueError(f"Stats for Pokemon '{pokemon_name}' not found")

        response.raise_for_status()

        log_event(
            api=api,
            function=function,
            message=(
                f"END pokemon={pokemon_name} status=200 "
                f"latency_ms={latency_ms}"
            ),
        )

        return response.json()

    except ValueError:
        raise

    except httpx.HTTPError as exc:
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

        raise RuntimeError("Error calling Poke Stats Service")

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