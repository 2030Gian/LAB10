from typing import Optional

from pydantic import BaseModel


class ImageResponse(BaseModel):
    name: str
    image_url: Optional[str] = None
    source: Optional[str] = None


class ErrorResponse(BaseModel):
    detail: str
