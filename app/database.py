from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config.config import config

DB_PATH = f"postgresql://{config.database.user}:" \
          f"{config.database.password}@" \
          f"{config.database.host}:" \
          f"{config.database.port}/" \
          f"{config.database.name}"

Base = declarative_base()
engine = create_engine(DB_PATH, pool_pre_ping=True)
SwssionClass = sessionmaker(bind=engine)
session = SwssionClass()
