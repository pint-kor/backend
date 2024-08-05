from fastapi import APIRouter, Path, Query, Depends
from .models import Blog, BlogAPI
from ..auth.models import User
from typing import List
from bson import ObjectId
from typing import Union
from ..auth.libs import current_active_user
from .exceptions import NOT_WRITER_ERROR

router = APIRouter()

@router.get("/blog", tags=["blog"], description="placeId 지정시 다른 파라미터 무시. placeId 미지정시 다른 파라미터로 검색")
async def blog(
        placeId: Union[str, None] = Query(None),
        latitude: Union[float, None] = Query(None),
        longitude: Union[float, None] = Query(None),
        radius: Union[int, None] = Query(None),
    ) -> List[Blog]:
    
    
    if placeId:
        return await Blog.find(Blog.placeId == placeId, limit=20).to_list()
        
    if all([latitude, longitude, radius]):
        query = {}
        query["location"] = {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$maxDistance": radius
            }
        }
        return await Blog.find_many(query, limit=20).to_list()
    
    return await Blog.find_all().to_list()

@router.get("/blog/{item_id}", tags=["blog"], description="특정 블로그 포스트 가져오기")
async def blog_id(
    item_id: str = Path(title = "The ID of the post to get"),
) -> Blog | None: 
    blog = await Blog.get(item_id)
    return blog

@router.post("/blog", tags=["blog"], description="블로그 포스트 작성")
async def blog_post(blogAPI: BlogAPI, user: User = Depends(current_active_user)):
    
    # casting BlogAPI to Blog
    blog = Blog(
        location=blogAPI.location,
        content=blogAPI.content,
        visited_at=blogAPI.visited_at,
        placeId=blogAPI.placeId,
        isPrivate=blogAPI.isPrivate,
        writer=user.id
    )
    
    document = await Blog.insert(blog)
    user.myPosts.append(document.id)
    await user.save()
    return document

@router.delete("/blog/{item_id}", tags=["blog"], description="블로그 포스트 삭제")
async def blog_delete(
    item_id: str = Path(title = "The ID of the post to delete"),
    user: User = Depends(current_active_user)
):
    blog = await Blog.get(item_id)
    
    if (blog.writer != user.id):
        raise NOT_WRITER_ERROR
    
    user.myPosts.remove(blog.id)
    await user.save()
    await blog.delete()
    return True

@router.patch("/blog/{item_id}", tags=["blog"], description="블로그 포스트 수정")
async def blog_patch(
        blogAPI: BlogAPI,
        item_id: str = Path(title = "The ID of the post to update"),
        user: User = Depends(current_active_user)
    ):
    blog = await Blog.get(item_id)
    
    if (blog.writer != user.id):
        raise NOT_WRITER_ERROR
    
    blog.content = blogAPI.content
    blog.visited_at = blogAPI.visited_at
    blog.placeId = blogAPI.placeId
    blog.isPrivate = blogAPI.isPrivate
    
    return await blog.save()

@router.patch("/blog/heart/{item_id}", tags=["blog"], description="좋아요")
async def blog_heart(
    active: bool = Query(True),
    item_id: str = Path(title = "The ID of the post to like"),
    user: User = Depends(current_active_user)
):
    
    blog = await Blog.get(item_id)
    
    if active and ObjectId(item_id) not in user.heartPosts:
        blog.heartCount += 1
        user.heartPosts.append(ObjectId(item_id))
        await blog.save()
        await user.save()
    elif not active and ObjectId(item_id) in user.heartPosts:
        blog.heartCount -= 1
        user.heartPosts.remove(ObjectId(item_id))
        await blog.save()
        await user.save()   
    
    return blog.heartCount

@router.patch("/blog/bookmark/{item_id}", tags=["blog"], description="북마크")
async def blog_bookmark(
    active: bool = Query(True),
    item_id: str = Path(title = "The ID of the post to bookmark"),
    user: User = Depends(current_active_user)
):
    
    blog = await Blog.get(item_id)
    
    if active and ObjectId(item_id) not in user.bookMarkPosts:
        blog.bookMarkCount += 1
        user.bookMarkPosts.append(ObjectId(item_id))
        await blog.save()
        await user.save()
    elif not active and ObjectId(item_id) in user.bookMarkPosts:
        blog.bookMarkCount -= 1
        user.bookMarkPosts.remove(ObjectId(item_id))
        await blog.save()
        await user.save()    
    
    return blog.bookMarkCount