# Poke Stats Service

Microservicio FastAPI encargado de devolver las estadísticas de un Pokémon.

## Endpoints

### Health Check

GET /health

### Get Pokemon Stats

GET /stats/{pokemon_name}

Ejemplo:

GET /stats/charizard

## Instalación local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt