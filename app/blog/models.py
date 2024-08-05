from ..base.models import AppBaseModel
from beanie import Document, PydanticObjectId
from beanie.operators import GeoWithin, Near
from ..auth.models import User
from datetime import datetime
from pydantic import Field
from ..base.models import PyObjectId
from typing import Optional, List, Tuple
import pymongo

class GeoObject(AppBaseModel):
    type: str = Field(default="Point")
    coordinates: Tuple[float, float]

class BlogAPI(AppBaseModel, Document):
    content: str
    visited_at: datetime = Field(default_factory=datetime.now)
    placeId: str = Field(default="")
    location: Optional[GeoObject] = Field(default=None)
    isPrivate: Optional[bool] = Field(default=False)
    
class Blog(BlogAPI):
    writer: PydanticObjectId
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    heartCount: int = Field(default=0)
    bookMarkCount: int = Field(default=0)
    images: List[str] = Field(default_factory=list)
    
    class Settings:
        indexes = [
            [("location", pymongo.GEOSPHERE)]
        ]
    
async def read(id: Optional[int]) -> List[Blog]:
    if (id.is_valid()):
        blog = await Blog.get(id)
        return [blog]
    
    blogs = await Blog.find_all().to_list()
    return blogs