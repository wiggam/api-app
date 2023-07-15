# working with environment variables
from pydantic import BaseSettings

# setting invironment variables, validation of variables
class Settings(BaseSettings):
    database_hostname: str 
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # sets the environment varaibles from our .env file
    class Config:
        env_file = ".env"

# creating the setttings instance
settings = Settings()
