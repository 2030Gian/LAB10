import os
import random
from gevent.lock import Semaphore

from locust import HttpUser, task, between, events


TARGET_REQUESTS = int(os.getenv("TARGET_REQUESTS", "5000"))

POKEMONS = [
    "charizard",
    "pikachu",
    "bulbasaur",
    "charmander",
    "squirtle",
    "mewtwo",
    "eevee",
    "snorlax",
]

request_count = 0
stop_requested = False
lock = Semaphore()
locust_environment = None


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    global locust_environment
    locust_environment = environment


@events.request.add_listener
def on_request_finished(**kwargs):
    global request_count, stop_requested

    with lock:
        request_count += 1

        if request_count >= TARGET_REQUESTS and not stop_requested:
            stop_requested = True
            print(f"\nTarget reached: {request_count} requests. Stopping Locust...\n")

            if locust_environment and locust_environment.runner:
                locust_environment.runner.quit()


class SearchApiUser(HttpUser):
    wait_time = between(0.1, 0.3)

    @task
    def search_pokemon(self):
        pokemon_name = random.choice(POKEMONS)

        self.client.post(
            "/poke/search",
            json={
                "pokemon_name": pokemon_name
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            name="POST /poke/search",
        )