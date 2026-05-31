from pathlib import Path
from typing import Optional
from app.core.config import settings
from app.utils.normalize import normalize_name


ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def get_images_root() -> Path:
    root = Path(settings.IMAGES_DIR)
    root.mkdir(parents=True, exist_ok=True)
    return root


def find_image_by_pokemon_name(pokemon_name: str) -> Optional[Path]:
    images_root = get_images_root()
    target_name = normalize_name(pokemon_name)

    if not target_name:
        return None

    for file_path in images_root.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        file_stem = normalize_name(file_path.stem)
        parent_name = normalize_name(file_path.parent.name)

        if file_stem == target_name or parent_name == target_name:
            return file_path

    return None


def get_relative_image_path(image_path: Path) -> str:
    images_root = get_images_root()
    return image_path.relative_to(images_root).as_posix()