from sqlalchemy import String, Integer, Column, Boolean

from app.database import Base, engine


class Plant(Base):
    __tablename__ = "plants"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    active: bool = Column(Boolean, default=True)
    category: str = Column(String)
    name: str = Column(String)
    description: str = Column(String)
    price: int = Column(Integer)
    photo_id: str = Column(String, unique=True)

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
