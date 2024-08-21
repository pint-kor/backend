from datetime import datetime
from enum import Enum
from typing import List, Optional

from beanie import PydanticObjectId, Document
from pydantic import Field, EmailStr, SecretStr
from app.base.models import AppBaseModel
from fastapi_users import schemas
from fastapi_users_db_beanie import BeanieBaseUser, BaseOAuthAccount

class OAuthAccount(BaseOAuthAccount):
    pass

class User(BeanieBaseUser, Document, AppBaseModel):
    oauth_accounts: List[OAuthAccount] = Field(default_factory=list)
    
    email: EmailStr
    hashed_password: str
    
    username: Optional[str] = Field(None, description='Username')
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    picture: Optional[str] = Field(None)
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_login_at: datetime = Field(default_factory=datetime.now)
    
    myPosts: List[PydanticObjectId] = Field(default_factory=list)
    heartPosts: List[PydanticObjectId] = Field(default_factory=list)
    bookMarkPosts: List[PydanticObjectId] = Field(default_factory=list)
    followers: List[PydanticObjectId] = Field(default_factory=list)
    following: List[PydanticObjectId] = Field(default_factory=list)
    
class UserInfo(AppBaseModel, Document):
    email: EmailStr
    username: Optional[str]
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime
    myPosts: List[PydanticObjectId]
    heartPosts: List[PydanticObjectId]
    bookMarkPosts: List[PydanticObjectId]
    followers: List[PydanticObjectId]
    following: List[PydanticObjectId]
    

    
class UserRead(schemas.BaseUser[PydanticObjectId], User):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    pass
    