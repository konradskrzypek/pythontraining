from pydantic import BaseSettings, PostgresDsn, Field


class Settings(BaseSettings):
    db_url: PostgresDsn = Field('postgresql://root:root@localhost:5432/models', env="MLSERVER_DB_URL")
