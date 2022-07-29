from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from mlserver.configuration import Settings


Base = declarative_base()
engine = create_engine(Settings().db_url)
