from pydantic import BaseSettings

class Settings(BaseSettings):
    version: str = "0.3.0"
    app_name: str = "fastapi svelte dashboard"
    admin_email: str = "aaa@bbb.com"
    db_host: str = "localhost:3306"
    db_user: str = "userid"
    db_pass: str = "userpw"
    env: str = "dev"
    db_conn_token: str = None

    class Config:
        env_file = ".env"

