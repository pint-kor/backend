from ..base.models import AppBaseModel
from beanie import Document, PydanticObjectId
from pydantic import Field
from typing import Optional, Tuple
import pymongo


class GeoObject(AppBaseModel):
    type: str = Field(default="Point")
    coordinates: Tuple[float, float]

class Place(AppBaseModel, Document):
    googlePlaceId: str = Field(default="")
    placeName: str = Field(default="")
    location: Optional[GeoObject] = Field(default=None)

    class Settings:
        indexes = [
            [("location", pymongo.GEOSPHERE)],
            [("placeName", pymongo.TEXT)]
        ]
