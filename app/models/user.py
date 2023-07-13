from sqlalchemy import String, Integer, Column, Boolean, BIGINT, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base, engine


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    tg_id: int = Column(BIGINT)


class Like(Base):
    __tablename__ = "likes"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(Integer)
    user_id = Column(BIGINT, ForeignKey('users.id'))
    user = relationship("User", backref="liked")


# Base.metadata.drop("liked")
Base.metadata.create_all(engine)
