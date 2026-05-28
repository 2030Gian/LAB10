from pathlib import Path

from app.core.config import settings
from app.models.schemas import ImageResponse
from app.utils.normalize import normalize_name


def find_image_by_name(pokemon_name: str) -> ImageResponse | None:
    normalized_name = normalize_name(pokemon_name)
    images_dir = Path(settings.IMAGES_DIR)

    for extension in ("png", "jpg", "jpeg", "webp", "gif"):
        candidate = images_dir / f"{normalized_name}.{extension}"

        if candidate.exists():
            return ImageResponse(
                name=normalized_name,
                image_url=str(candidate),
                source="local",
            )

    return None
