import time
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from logger import get_logger

app = FastAPI(title="Search API - MonitorMach")
logger = get_logger("SearchAPI")

POKE_API_BASE = "https://pokeapi.co/api/v2/pokemon"


# ---------- Schemas ----------

class SearchRequest(BaseModel):
    Pokemon_Name: str

class SearchResponse(BaseModel):
    name: str


# ---------- Endpoint ----------

@app.post("/poke/search", response_model=SearchResponse)
async def search_pokemon(request: SearchRequest):
    pokemon_name = request.Pokemon_Name.strip().lower()
    logger.info(f"[START] search_pokemon | input='{pokemon_name}'")
    t_start = time.time()

    url = f"{POKE_API_BASE}/{pokemon_name}/"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            logger.info(f"[REQUEST] PokeAPI | url='{url}'")
            t_req = time.time()

            response = await client.get(url)
            latency_ms = round((time.time() - t_req) * 1000, 2)

            logger.info(f"[RESPONSE] PokeAPI | status={response.status_code} | latency={latency_ms}ms")

            if response.status_code == 404:
                logger.warning(f"[NOT_FOUND] Pokemon '{pokemon_name}' not found")
                raise HTTPException(status_code=404, detail=f"Pokemon '{pokemon_name}' not found")

            if response.status_code != 200:
                logger.error(f"[ERROR] PokeAPI returned status={response.status_code}")
                raise HTTPException(status_code=500, detail="Error calling PokeAPI")

            data = response.json()

    except httpx.RequestError as e:
        logger.error(f"[ERROR] Network error | error='{e}'")
        raise HTTPException(status_code=500, detail="Network error contacting PokeAPI")

    total_ms = round((time.time() - t_start) * 1000, 2)
    logger.info(f"[END] search_pokemon | name='{data['name']}' | total_latency={total_ms}ms")

    return SearchResponse(name=data["name"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "SearchAPI"}