import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DEFAULT_DB_URL = 'postgresql://root:root@localhost:5432/models'

Base = declarative_base()
db_url = os.getenv('MLSERVER_DATABASE_URL', default=DEFAULT_DB_URL)
engine = create_engine(db_url)
