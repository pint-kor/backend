from fastapi import APIRouter, Depends
from .libs import fastapi_users, auth_backend, current_active_user
from .models import User, UserCreate, UserRead, UserUpdate, UserInfo
from ..blog.models import Blog
from .kakao.routes import kakao_oauth_router
from fastapi import HTTPException, Query
from typing import Union, Optional, List
from bson import ObjectId

router = APIRouter()

get_auth_router = fastapi_users.get_auth_router(auth_backend)
get_register_router = fastapi_users.get_register_router(UserRead, UserCreate)
get_reset_password_router = fastapi_users.get_reset_password_router()
get_verify_router = fastapi_users.get_verify_router(UserRead)
get_users_router = fastapi_users.get_users_router(UserRead, UserUpdate)

routers = [
    (router, dict(prefix="/auth", tags=["auth"])),
    (get_auth_router, dict(prefix="/auth/jwt", tags=["auth"])),
    (get_register_router, dict(prefix="/auth", tags=["auth"])),
    (get_reset_password_router, dict(prefix="/auth", tags=["auth"])),
    (get_verify_router, dict(prefix="/auth", tags=["auth"])),
    (kakao_oauth_router, dict(prefix="/auth/kakao", tags=["auth"])),
    (get_users_router, dict(prefix="/users", tags=["users"]))
]

@router.get("/authenticated-route")
async def authenticated_route(user = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

@get_users_router.get("", response_model=List[UserInfo], tags=["users"])
async def users(
    username: str = Query(None)
) -> List[UserInfo]: 
    # get by username similar
    user = User.find({
        "username": {"$regex": username, "$options": "i"},
    })
    
    return await user.to_list()

@get_users_router.post("/follow/{userId}", tags=["users"])
async def follow_user(userId: str, user: User = Depends(current_active_user)) -> User:
    following_user = await User.get(userId)
    
    if not following_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if userId in user.following:
        raise HTTPException(status_code=400, detail="Already following")
    
    if user.id in following_user.followers:
        raise HTTPException(status_code=400, detail="Already followed")
    
    following_user.followers.append(ObjectId(user.id)) 
    user.following.append(ObjectId(userId))
    
    await following_user.save()
    await user.save()
    return user

@get_users_router.post("/unfollow/{userId}", tags=["users"])
async def unfollow_user(userId: str, user: User = Depends(current_active_user)) -> User:
    following_user = await User.get(userId)
    if not following_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        following_user.followers.remove(ObjectId(user.id))
        await following_user.save()
    except ValueError:
        pass
    
    try:
        user.following.remove(ObjectId(userId))
        await user.save()
    except ValueError:
        pass
    
    return user

@get_users_router.post("/sync", tags=["users"])
async def sync_users(user: User = Depends(current_active_user)) -> User:
    heartPosts = user.heartPosts
    bookMarkPosts = user.bookMarkPosts
    
    for postId in heartPosts:
        # check if the post exists
        post = await Blog.get(postId)
        if post:
            user.heartPosts.remove(postId)
            
    for postId in bookMarkPosts:
        # check if the post exists
        post = await Blog.get(postId)
        if post:
            user.bookMarkPosts.remove(postId)
            
    await user.save()
    return user
    