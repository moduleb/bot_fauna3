from sqlalchemy import func
from sqlalchemy.orm import Session

from app.logger import logger
from app.models.plant import Plant
from app.models.user import User, Like


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def get_one(self, tg_id):
        try:
            return self.session.query(User).filter(User.tg_id == tg_id).first()
        except Exception as e:
            logger.error(f"DB error: {e}")

    def create(self, tg_id):
        user = User(tg_id=tg_id)
        logger.info(f'Пользователь id: {tg_id} сохранен в бд')
        self.session.add(user)
        self.session.commit()

    def like(self, user_id, plant_id):
        logger.debug(f"Create Like obj. user_id: {user_id}, plant_id: {plant_id} ")
        like = Like(user_id=user_id, plant_id=plant_id)
        self.session.add(like)
        self.session.commit()

    def dislike(self, user_id, plant_id):
        logger.debug("dislike")
        like = self.check_like(user_id, plant_id)
        logger.debug(like)
        if like:
            self.session.delete(like)
        self.session.commit()

    def get_all(self, user_id):
        return self.session.query(Like).filter(Like.user_id == user_id).all()

    def check_like(self, user_id, plant_id):
        logger.debug("check_like")
        return self.session.query(Like).filter(Like.user_id == user_id, Like.plant_id == plant_id).first()
