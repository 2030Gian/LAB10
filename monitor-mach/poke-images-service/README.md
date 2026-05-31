# Poke Images Service

Microservicio FastAPI encargado de devolver la imagen de un Pokémon.

## Endpoints

### Health Check

GET /health

### Get Pokemon Image

GET /images/{pokemon_name}

Ejemplo:

GET /images/charizard

## Estructura esperada de imágenes

Puedes usar cualquiera de estas formas:

```txt
data/images/charizard.png
data/images/Charizard.jpg
data/images/Charizard/image1.png
data/images/PokemonData/Charizard/0001.jpg