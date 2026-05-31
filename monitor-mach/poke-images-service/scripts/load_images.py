import argparse
import csv
import re
import shutil
import zipfile
from pathlib import Path


ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

GENERIC_FOLDER_NAMES = {
    "data",
    "images",
    "raw_images",
    "pokemondata",
    "pokemon",
    "dataset",
    "archive",
    "_extracted",
}


def normalize_name(value: str) -> str:
    if value is None:
        return ""

    value = value.strip().lower()
    value = value.replace("♀", "f")
    value = value.replace("♂", "m")
    value = re.sub(r"[^a-z0-9]", "", value)

    return value


def read_allowed_pokemon_names(stats_csv_path: str | None) -> set[str]:
    if not stats_csv_path:
        return set()

    csv_path = Path(stats_csv_path)

    if not csv_path.exists():
        print(f"[WARN] Stats CSV not found: {stats_csv_path}")
        return set()

    names = set()

    with open(csv_path, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row.get("Name") or row.get("name")

            if name:
                names.add(normalize_name(name))

    return names


def extract_zip_if_needed(source_path: Path, extract_dir: Path) -> Path:
    if source_path.is_file() and source_path.suffix.lower() == ".zip":
        extract_dir.mkdir(parents=True, exist_ok=True)

        print(f"[INFO] Extracting ZIP: {source_path}")
        print(f"[INFO] Extract dir: {extract_dir}")

        with zipfile.ZipFile(source_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        return extract_dir

    return source_path


def find_image_files(source_dir: Path) -> list[Path]:
    image_files = []

    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        image_files.append(file_path)

    return image_files


def infer_pokemon_name_from_path(image_path: Path, source_root: Path) -> str:
    """
    Soporta datasets tipo:

    PokemonData/Charizard/0001.png
    PokemonData/Pikachu/image.jpg
    images/charizard.png
    images/Charizard.jpg
    """

    parent_name = normalize_name(image_path.parent.name)
    file_stem = normalize_name(image_path.stem)

    if parent_name and parent_name not in GENERIC_FOLDER_NAMES:
        return parent_name

    return file_stem


def load_images(
    source: str,
    output_dir: str,
    stats_csv: str | None = None,
    overwrite: bool = False,
):
    source_path = Path(source)
    output_path = Path(output_dir)
    extract_dir = Path("data/raw_images/_extracted")

    if not source_path.exists():
        raise FileNotFoundError(f"Source not found: {source}")

    output_path.mkdir(parents=True, exist_ok=True)

    source_root = extract_zip_if_needed(source_path, extract_dir)
    image_files = find_image_files(source_root)

    allowed_names = read_allowed_pokemon_names(stats_csv)

    copied = 0
    skipped = 0
    manifest_rows = []

    used_names = set()

    for image_file in image_files:
        pokemon_name = infer_pokemon_name_from_path(image_file, source_root)
        normalized_name = normalize_name(pokemon_name)

        if not normalized_name:
            skipped += 1
            continue

        if allowed_names and normalized_name not in allowed_names:
            skipped += 1
            continue

        if normalized_name in used_names:
            skipped += 1
            continue

        extension = image_file.suffix.lower()
        output_file = output_path / f"{normalized_name}{extension}"

        if output_file.exists() and not overwrite:
            skipped += 1
            used_names.add(normalized_name)
            continue

        shutil.copy2(image_file, output_file)

        manifest_rows.append(
            {
                "pokemon_name": pokemon_name,
                "normalized_name": normalized_name,
                "source_path": str(image_file),
                "output_path": str(output_file),
            }
        )

        used_names.add(normalized_name)
        copied += 1

    manifest_file = output_path.parent / "images_manifest.csv"

    with open(manifest_file, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "pokemon_name",
            "normalized_name",
            "source_path",
            "output_path",
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    print("[INFO] Image loading finished.")
    print(f"[INFO] Source: {source}")
    print(f"[INFO] Output: {output_dir}")
    print(f"[INFO] Copied: {copied}")
    print(f"[INFO] Skipped: {skipped}")
    print(f"[INFO] Manifest: {manifest_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source",
        required=True,
        help="Path to image dataset folder or ZIP file",
    )

    parser.add_argument(
        "--output",
        default="data/images",
        help="Output folder for normalized images",
    )

    parser.add_argument(
        "--stats-csv",
        default=None,
        help="Optional pokemon_stats.csv to filter only valid Pokemon names",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite images if they already exist",
    )

    args = parser.parse_args()

    load_images(
        source=args.source,
        output_dir=args.output,
        stats_csv=args.stats_csv,
        overwrite=args.overwrite,
    )