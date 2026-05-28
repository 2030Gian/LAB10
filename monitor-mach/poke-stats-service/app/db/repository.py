from typing import Optional, Dict, Any
from app.db.connection import get_connection


def find_pokemon_stats_by_name(pokemon_name: str) -> Optional[Dict[str, Any]]:
    query = """
        SELECT
            pokedex_id,
            name,
            type_1,
            type_2,
            total,
            hp,
            attack,
            defense,
            sp_attack,
            sp_defense,
            speed,
            generation,
            legendary
        FROM pokemon_stats
        WHERE lower(name) = lower(?)
        LIMIT 1;
    """

    with get_connection() as connection:
        cursor = connection.execute(query, (pokemon_name,))
        row = cursor.fetchone()

    if row is None:
        return None

    return dict(row)