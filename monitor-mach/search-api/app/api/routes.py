from fastapi import APIRouter, HTTPException

from app.models.schemas import PokemonSearchRequest, PokemonSearchResponse
from app.services.search_service import search_pokemon

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "service": "SearchAPI",
        "status": "UP"
    }


@router.post(
    "/poke/search",
    response_model=PokemonSearchResponse,
    responses={
        404: {"description": "Pokemon not found"},
        502: {"description": "Error calling downstream service"},
        500: {"description": "Internal server error"},
    },
)
async def poke_search(request: PokemonSearchRequest):
    pokemon_name = request.pokemon_name.strip()

    if not pokemon_name:
        raise HTTPException(
            status_code=400,
            detail="pokemon_name is required"
        )

    try:
        return await search_pokemon(pokemon_name)

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )