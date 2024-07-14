from ..base.models import AppBaseModel
from beanie import Document, PydanticObjectId
from ..auth.models import User
from datetime import datetime
from pydantic import Field
from ..base.models import PyObjectId
from typing import Optional, List

class Blog(Document, AppBaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    writer: PydanticObjectId
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    placeId: str = Field(default="")
    
async def read(id: Optional[int]) -> List[Blog]:
    if (id.is_valid()):
        blog = await Blog.get(id)
        return [blog]
    
    blogs = await Blog.find_all().to_list()
    return blogs