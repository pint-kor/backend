from fastapi import APIRouter, Depends
from .libs import fastapi_users, auth_backend, current_active_user
from .models import User, UserCreate, UserRead, UserUpdate
from .kakao.routes import kakao_oauth_router

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