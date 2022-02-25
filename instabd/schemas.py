from datetime import datetime
from datetime import timedelta
from enum import Enum
from typing import List
from typing import Optional

from pydantic import BaseModel


class MediaType(Enum):
    image = "IMAGE"
    video = "VIDEO"
    carousel_album = "CAROUSEL_ALBUM"


class Authentication(BaseModel):
    access_token: str
    expires_at: Optional[datetime] = None

    def __init__(self, **data):
        expires_in = data.get("expires_in", None)
        if expires_in:
            data["expires_at"] = datetime.now() + timedelta(seconds=expires_in)
        super().__init__(**data)


class User(BaseModel):
    id: str
    username: str


class Children(BaseModel):
    id: str
    media_type: str
    media_url: str
    permalink: str
    thumbnail_url: Optional[str] = None
    timestamp: str
    username: str


class Media(BaseModel):
    id: str
    caption: Optional[str] = None
    media_type: str
    media_url: str
    permalink: str
    thumbnail_url: Optional[str] = None
    timestamp: str
    username: str
    children: Optional[List[Children]] = []