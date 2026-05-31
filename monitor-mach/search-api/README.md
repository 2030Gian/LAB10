# Search API

API principal que recibe búsquedas de Pokémon y orquesta llamadas a:

- PokeAPI externa
- Poke Stats Service
- Poke Images Service

## Endpoint principal

POST /poke/search

Body:

```json
{
  "pokemon_name": "charizard"
}