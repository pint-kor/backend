from fastapi import APIRouter, Path, Query
from .models import read, Blog
from typing import List
from beanie import PydanticObjectId
from bson import ObjectId
from typing import Union

router = APIRouter()

@router.get("/blog", tags=["blog"])
async def blog(
        placeId: Union[str, None] = Query(None),
    ) -> List[Blog]:
    
    return await Blog.find(Blog.placeId == placeId).to_list()

@router.get("/blog/{item_id}", tags=["blog"])
async def blog_id(
    item_id: str = Path(title = "The ID of the post to get"),
) -> List[Blog]:
    return await Blog.find({
        "_id": ObjectId(item_id)
    }).to_list()

@router.post("/blog", tags=["blog"])
async def blog_post(blog: Blog):
    await blog.save()

@router.delete("/blog/{item_id}", tags=["blog"])
async def blog_delete(
    item_id: str = Path(title = "The ID of the post to delete")
):
    blog = await Blog.find({
        "_id": ObjectId(item_id)
    }).to_list()
    
    if len(blog) == 0:
        return None
    
    await Blog.delete(blog[0])

@router.patch("/blog", tags=["blog"])
async def blog_patch(blog: Blog):
    return await Blog.update(blog)

@router.post("/blog-test", tags=["blog"])
async def blog_test():
    blog: Blog = Blog(
        writer=PydanticObjectId(),
        title="test",
        content="test"
    )
    
    await blog.save()