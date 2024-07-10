import os
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

def get_env_file():
    stage = os.environ.get('ENV') or 'dev'
    print(stage)
    return f'{stage}.env'

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding="utf-8"
    )
    
    DEBUG: bool = False
    
    APP_NAME: str = "pint"
    HTTPS: bool = False
    HOST: str = "localhost"
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DB_HOST: str
    DB_DATABASE: str
    DB_URL: str
    
    ORIGINS: List[str] = Field(['http://localhost'], env="ORIGINS")
    ALLOWED_HOSTS: List[str] = Field(..., env="ALLOWED_HOSTS")
    
    KAKAO_CLIENT_ID: str = None
    KAKAO_CLIENT_SECRET: str = None
    KAKAO_CALLBACK_URL: str = None
        
    @property
    def URL(self) -> str:
        protocol = 'https' if self.HTTPS else 'http'
        return f"{protocol}://{self.HOST}"
    
Configs = Settings()

print('Configs:\n', Configs)

@lru_cache()
def get_settings():
    return Settings()
    