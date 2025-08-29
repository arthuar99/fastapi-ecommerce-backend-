from pydantic import BaseSettings

class Settings(BaseSettings):
    DAATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_Algorithm:str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = "FastAPI E-Commerce"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"


    Settings = Settings()