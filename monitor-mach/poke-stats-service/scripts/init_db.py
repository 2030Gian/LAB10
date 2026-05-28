import argparse
import csv
import sqlite3
from pathlib import Path


def clean_int(value):
    if value is None or value == "":
        return None

    try:
        return int(float(value))
    except ValueError:
        return None


def clean_bool(value):
    if value is None:
        return False

    return str(value).strip().lower() in ["true", "1", "yes"]


def get_value(row, *possible_keys):
    for key in possible_keys:
        if key in row:
            return row[key]
    return None


def init_database(csv_path: str, db_path: str):
    csv_file = Path(csv_path)
    database_file = Path(db_path)

    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    database_file.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(database_file))
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS pokemon_stats;")

    cursor.execute("""
        CREATE TABLE pokemon_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pokedex_id INTEGER,
            name TEXT NOT NULL,
            type_1 TEXT,
            type_2 TEXT,
            total INTEGER,
            hp INTEGER,
            attack INTEGER,
            defense INTEGER,
            sp_attack INTEGER,
            sp_defense INTEGER,
            speed INTEGER,
            generation INTEGER,
            legendary BOOLEAN
        );
    """)

    with open(csv_file, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        inserted = 0

        for row in reader:
            name = get_value(row, "Name", "name")

            if not name:
                continue

            cursor.execute(
                """
                INSERT INTO pokemon_stats (
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
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    clean_int(get_value(row, "#", "id", "pokedex_id")),
                    name.strip(),
                    get_value(row, "Type 1", "type_1"),
                    get_value(row, "Type 2", "type_2"),
                    clean_int(get_value(row, "Total", "total")),
                    clean_int(get_value(row, "HP", "hp")),
                    clean_int(get_value(row, "Attack", "attack")),
                    clean_int(get_value(row, "Defense", "defense")),
                    clean_int(get_value(row, "Sp. Atk", "sp_attack", "Sp Atk")),
                    clean_int(get_value(row, "Sp. Def", "sp_defense", "Sp Def")),
                    clean_int(get_value(row, "Speed", "speed")),
                    clean_int(get_value(row, "Generation", "generation")),
                    clean_bool(get_value(row, "Legendary", "legendary")),
                ),
            )

            inserted += 1

    connection.commit()
    connection.close()

    print(f"Database initialized successfully.")
    print(f"CSV: {csv_path}")
    print(f"DB: {db_path}")
    print(f"Rows inserted: {inserted}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/pokemon_stats.csv")
    parser.add_argument("--db", default="data/poke_stats.db")

    args = parser.parse_args()

    init_database(args.csv, args.db)