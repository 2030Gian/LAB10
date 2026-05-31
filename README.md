Monitor Mach - Laboratorio 10 Arquitectura de Software

Proyecto backend basado en microservicios para consultar información de Pokémon, generar logs distribuidos, ejecutar pruebas de carga y procesar métricas mediante un bot/CLI.

El sistema implementa una arquitectura donde una API principal llamada search-api orquesta llamadas a:

PokeAPI externa
poke-stats-service
poke-images-service

Además, cada microservicio genera sus propios logs con una nomenclatura estándar para luego ser procesados por monitor-bot.

Arquitectura
Cliente / Load Test / Bot
        |
        v
POST /poke/search
        |
        v
Search API
   |-----------------------> PokeAPI externa
   |
   |-----------------------> Poke Stats Service ---> SQLite / CSV
   |
   |-----------------------> Poke Images Service --> File Server local
Microservicios
1. Search API

Servicio principal encargado de recibir la búsqueda del Pokémon y orquestar las llamadas a los demás servicios.

Puerto local:

8000

Endpoints:

GET  /health
POST /poke/search

Ejemplo:

curl -X POST http://localhost:8000/poke/search \
  -H "Content-Type: application/json" \
  -d '{"pokemon_name":"charizard"}'

Respuesta esperada:

{
  "name": "charizard",
  "pokedex_id": 6,
  "types": ["fire", "flying"],
  "abilities": ["blaze", "solar-power"],
  "stats": {
    "pokedex_id": 6,
    "name": "Charizard",
    "type_1": "Fire",
    "type_2": "Flying",
    "total": 534,
    "hp": 78,
    "attack": 84,
    "defense": 78,
    "sp_attack": 109,
    "sp_defense": 85,
    "speed": 100,
    "generation": 1,
    "legendary": false
  },
  "image_url": "http://localhost:8002/static/images/charizard.png"
}
2. Poke Stats Service

Microservicio encargado de devolver las estadísticas del Pokémon usando un dataset CSV cargado en SQLite.

Puerto local:

8001

Endpoints:

GET /health
GET /stats/{pokemon_name}

Ejemplo:

curl http://localhost:8001/stats/charizard

Respuesta esperada:

{
  "pokedex_id": 6,
  "name": "Charizard",
  "type_1": "Fire",
  "type_2": "Flying",
  "total": 534,
  "hp": 78,
  "attack": 84,
  "defense": 78,
  "sp_attack": 109,
  "sp_defense": 85,
  "speed": 100,
  "generation": 1,
  "legendary": false
}
3. Poke Images Service

Microservicio encargado de devolver la URL de la imagen del Pokémon usando imágenes almacenadas localmente.

Puerto local:

8002

Endpoints:

GET /health
GET /images/{pokemon_name}

Ejemplo:

curl http://localhost:8002/images/charizard

Respuesta esperada:

{
  "name": "charizard",
  "image_url": "http://localhost:8002/static/images/charizard.png",
  "relative_path": "/static/images/charizard.png"
}
4. Monitor Bot

CLI encargado de procesar los logs generados por los microservicios y calcular métricas.

Comandos implementados:

CheckLatency
CheckAvailability
RenderGraph
Stats
Estructura del repositorio
monitor-mach/
│
├── search-api/
│   ├── app/
│   ├── logs/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── poke-stats-service/
│   ├── app/
│   ├── data/
│   │   ├── pokemon_stats.csv
│   │   └── poke_stats.db
│   ├── logs/
│   ├── scripts/
│   │   └── init_db.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── poke-images-service/
│   ├── app/
│   ├── data/
│   │   └── images/
│   ├── logs/
│   ├── scripts/
│   │   └── load_images.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── monitor-bot/
│   ├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
├── load-test/
│   ├── locustfile.py
│   ├── requirements.txt
│   └── results/
│
├── docker-compose.yml
├── .gitignore
└── README.md
Requisitos

Para ejecutar el proyecto se necesita:

Docker
Docker Compose
Python 3.12 o superior

Opcional para ejecutar scripts localmente:

pip
virtualenv o conda
Variables de entorno
Search API
SERVICE_NAME=SearchAPI
SERVICE_PORT=8000
POKE_API_BASE_URL=https://pokeapi.co/api/v2
POKE_STATS_BASE_URL=http://poke-stats-service:8001
POKE_IMAGES_BASE_URL=http://poke-images-service:8002
HTTP_TIMEOUT_SECONDS=10
LOG_FILE=logs/search-api.log
LOG_LEVEL=INFO
Poke Stats Service
SERVICE_NAME=PokeStats
SERVICE_PORT=8001
DATABASE_PATH=data/poke_stats.db
CSV_PATH=data/pokemon_stats.csv
LOG_FILE=logs/poke-stats-service.log
LOG_LEVEL=INFO
Poke Images Service
SERVICE_NAME=PokeImages
SERVICE_PORT=8002
IMAGES_DIR=data/images
PUBLIC_BASE_URL=http://localhost:8002
LOG_FILE=logs/poke-images-service.log
LOG_LEVEL=INFO
Ejecución con Docker Compose

Desde la raíz del repositorio:

docker compose up --build

Esto levanta:

search-api          -> http://localhost:8000
poke-stats-service  -> http://localhost:8001
poke-images-service -> http://localhost:8002

Para detener los servicios:

docker compose down
Verificar servicios

En otra terminal, ejecutar:

curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health

Respuestas esperadas:

{"service":"SearchAPI","status":"UP"}
{"service":"PokeStats","status":"UP"}
{"service":"PokeImages","status":"UP"}
Probar flujo completo

Ejecutar:

curl -X POST http://localhost:8000/poke/search \
  -H "Content-Type: application/json" \
  -d '{"pokemon_name":"charizard"}'

El resultado debe incluir:

name
pokedex_id
types
abilities
stats
image_url
Logs distribuidos

Cada microservicio genera sus propios logs:

search-api/logs/search-api.log
poke-stats-service/logs/poke-stats-service.log
poke-images-service/logs/poke-images-service.log

Formato estándar:

{Fecha} {Modulo} {API} {Funcion} Message

Ejemplo:

2026-05-30T22:30:00.123 SearchAPI /poke/search search_pokemon START pokemon=charizard
2026-05-30T22:30:00.245 SearchAPI /poke/search search_pokemon END pokemon=charizard status=200 latency_ms=122.5

Los logs incluyen:

timestamp
módulo
API
función
status code
latencia en ms
mensaje del evento
Ver logs
tail -n 20 search-api/logs/search-api.log
tail -n 20 poke-stats-service/logs/poke-stats-service.log
tail -n 20 poke-images-service/logs/poke-images-service.log

Contar líneas generadas:

wc -l search-api/logs/search-api.log
wc -l poke-stats-service/logs/poke-stats-service.log
wc -l poke-images-service/logs/poke-images-service.log
Pruebas de carga

El laboratorio solicita generar entre 1000 y 10000 llamadas para producir logs.

En este proyecto se puede usar Locust o JMeter.

Opción A: Locust
Estructura
load-test/
├── locustfile.py
├── requirements.txt
└── results/
Ejecutar Locust con Docker Compose

Crear carpeta de resultados:

mkdir -p load-test/results

Ejecutar Locust:

docker compose run --rm locust

El servicio Locust ejecuta 5000 requests contra:

POST http://search-api:8000/poke/search

Dentro de Docker Compose se usa:

http://search-api:8000

Desde la máquina host se usa:

http://localhost:8000
Opción B: Locust local

Instalar Locust:

python -m pip install -r load-test/requirements.txt

Ejecutar en modo headless:

TARGET_REQUESTS=5000 python -m locust \
  -f load-test/locustfile.py \
  --host http://127.0.0.1:8000 \
  --headless \
  -u 50 \
  -r 10 \
  --run-time 10m \
  --csv load-test/results/search-api-load-test

Parámetros:

TARGET_REQUESTS=5000  -> cantidad objetivo de requests
-u 50                 -> usuarios concurrentes
-r 10                 -> usuarios creados por segundo
--run-time 10m        -> tiempo máximo de ejecución
--csv                 -> exporta resultados
Opción C: JMeter

Configurar un Thread Group:

Number of Threads: 50
Ramp-up period: 20
Loop Count: 100

Total:

50 * 100 = 5000 requests

HTTP Request:

Protocol: http
Server Name or IP: 127.0.0.1
Port Number: 8000
Method: POST
Path: /poke/search

Body Data:

{
  "pokemon_name": "charizard"
}

Headers:

Content-Type: application/json
Accept: application/json

Guardar el archivo como:

load-test/search-api-load-test.jmx
Parte II - Monitor Bot

El bot procesa los logs generados por los microservicios.

Ubicación:

monitor-bot/

Instalar dependencias:

cd monitor-bot
python -m pip install -r requirements.txt
Comando: CheckLatency

Muestra la latencia promedio diaria de un módulo en un periodo determinado.

Ejemplo:

python main.py CheckLatency PokeStats --start-date 2026-05-30 --end-date 2026-05-30

Salida esperada:

Latency for module: PokeStats
30/05 12.45ms
Comando: CheckAvailability

Muestra la disponibilidad del servicio durante los últimos N días.

Fórmula:

Availability = Tasa de Éxito / (Tasa de Éxito + Tasa de Error)

Donde:

Tasa de Éxito = requests con status 200
Tasa de Error = requests con status 500

Ejemplo:

python main.py CheckAvailability PokeStats --last-days 5

Salida esperada:

Availability for module: PokeStats
30/05 99.9%
Comando: RenderGraph

Renderiza una gráfica en consola usando ASCII.

Ejemplo para latencia:

python main.py RenderGraph --metric Latency --module PokeStats --last-days 5

Ejemplo para disponibilidad:

python main.py RenderGraph --metric Availability --module PokeStats --last-days 5

Salida esperada:

Latency graph for PokeStats
===========================
30/05 | ████████████████████████████████████████ 12.45
Comando: Stats

Muestra métricas generales del módulo.

Ejemplo:

python main.py Stats PokeStats --last-days 5

Métricas incluidas:

P95 latency
requests per minute
error ratio
throughput
top failing endpoint
total requests
success count
error count
average latency
bottleneck
retry recommendation
scaling recommendation

Salida esperada:

Stats for module: PokeStats
P95 latency: 25.31 ms
Requests per minute: 450.5
Error ratio: 0.0%
Throughput: 450.5 successful req/min
Top failing endpoint: N/A
Total requests: 5000
Success count: 5000
Error count: 0
Average latency: 12.45 ms

Analysis
El bottleneck parece estar en PokeStats, con latencia promedio de 12.45 ms.
No se observan errores 500. No parece necesario agregar retry por ahora.
No parece necesario escalar todavía; el servicio se mantiene estable.
Módulos soportados por el bot

Se pueden consultar los siguientes módulos:

SearchAPI
PokeStats
PokeImages

Ejemplos:

python main.py Stats SearchAPI --last-days 5
python main.py Stats PokeStats --last-days 5
python main.py Stats PokeImages --last-days 5
Flujo recomendado para demostrar el laboratorio
1. Levantar servicios
docker compose up --build
2. Verificar health checks
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
3. Probar búsqueda
curl -X POST http://localhost:8000/poke/search \
  -H "Content-Type: application/json" \
  -d '{"pokemon_name":"charizard"}'
4. Generar carga

Con Locust:

docker compose run --rm locust

O local:

TARGET_REQUESTS=5000 python -m locust \
  -f load-test/locustfile.py \
  --host http://127.0.0.1:8000 \
  --headless \
  -u 50 \
  -r 10 \
  --run-time 10m \
  --csv load-test/results/search-api-load-test
5. Validar logs
wc -l search-api/logs/search-api.log
wc -l poke-stats-service/logs/poke-stats-service.log
wc -l poke-images-service/logs/poke-images-service.log
6. Ejecutar bot
cd monitor-bot

python main.py CheckLatency PokeStats --start-date 2026-05-30 --end-date 2026-05-30

python main.py CheckAvailability PokeStats --last-days 5

python main.py RenderGraph --metric Latency --module PokeStats --last-days 5

python main.py Stats PokeStats --last-days 5
Capturas sugeridas para entrega

Se recomienda adjuntar capturas de:

1. Docker Compose levantando los servicios.
2. Health checks de SearchAPI, PokeStats y PokeImages.
3. POST /poke/search funcionando.
4. GET /stats/charizard funcionando.
5. GET /images/charizard funcionando.
6. Locust o JMeter ejecutando 5000 requests.
7. Conteo de logs con wc -l.
8. Ejemplo de logs con tail.
9. CheckLatency.
10. CheckAvailability.
11. RenderGraph.
12. Stats.
Troubleshooting
Error: Invalid HTTP request received

Si aparece:

WARNING: Invalid HTTP request received.

Verificar que las URLs usen http y no https.

Correcto:

http://localhost:8000
http://poke-stats-service:8001
http://poke-images-service:8002

Incorrecto:

https://localhost:8000
https://poke-stats-service:8001
https://poke-images-service:8002
Error: Docker Compose no encuentra servicios

Verificar que el archivo docker-compose.yml tenga todos los servicios dentro de:

services:

Ejemplo:

services:
  search-api:
    ...

  poke-stats-service:
    ...

  poke-images-service:
    ...
Error: imágenes no encontradas

Verificar que existan imágenes en:

poke-images-service/data/images/

Ejemplo:

poke-images-service/data/images/charizard.png
poke-images-service/data/images/pikachu.png

También probar:

curl http://localhost:8002/images/charizard
Error: stats no encontrados

Verificar que exista:

poke-stats-service/data/pokemon_stats.csv

Y que la base de datos se haya generado:

poke-stats-service/data/poke_stats.db

Para regenerar la base de datos:

cd poke-stats-service
python scripts/init_db.py --csv data/pokemon_stats.csv --db data/poke_stats.db
Entregables

El repositorio debe incluir:

Código de los microservicios
Dockerfiles
docker-compose.yml
Dataset de stats o instrucciones para cargarlo
Scripts de inicialización
Locustfile o JMX
Monitor bot
README
Capturas de ejecución

No se recomienda subir imágenes pesadas, bases .db, logs generados ni carpetas temporales. Estos archivos deben estar en .gitignore.

Git Ignore recomendado
# Python
__pycache__/
*.py[cod]
*$py.class

# Entornos virtuales
.venv/
venv/
env/
ENV/

# Variables de entorno
.env
.env.*

# Logs
logs/
*.log
search-api/logs/
poke-stats-service/logs/
poke-images-service/logs/

# Pytest / coverage
.pytest_cache/
.coverage
htmlcov/

# Mac
.DS_Store

# SQLite / bases generadas
*.db
*.sqlite
*.sqlite3
poke-stats-service/data/*.db

# Archivos comprimidos pesados
*.zip
*.tar
*.tar.gz
*.rar
*.7z

# Datasets crudos e imágenes
poke-images-service/data/raw_images/
poke-images-service/data/images_manifest.csv
poke-images-service/data/images/*
!poke-images-service/data/images/.gitkeep

# Resultados pesados opcionales
load-test/results/*
!load-test/results/.gitkeep
Autores

Proyecto desarrollado para el Laboratorio 10 de Arquitectura de Software.

Equipo:

Monitor Mach