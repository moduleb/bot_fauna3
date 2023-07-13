from sqlalchemy import func
from sqlalchemy.orm import Session

from app.logger import logger
from app.models.plant import Plant


class PlantService:
    def __init__(self, session: Session):
        self.session = session

    def get_one(self, name):
        try:
            return self.session.query(Plant).filter(Plant.name == name).first()
        except Exception as e:
            logger.error(f"DB error: {e}")

    def get_one_by_id(self, plant_id):
        try:
            return self.session.query(Plant).filter(Plant.id == plant_id).first()
        except Exception as e:
            logger.error(f"DB error: {e}")

    def get_all(self):
        return self.session.query(Plant).order_by(Plant.name).all()

    def get_all_active(self):
        return self.session.query(Plant).filter_by(active=True).all()

    def get_all_categories(self):
        return self.session.query(Plant.category).group_by(Plant.category).all()

        # print(self.session.query(Plant.category).group_by(Plant.category).all())

    def get_all_active_by_category(self, category):
        return self.session.query(Plant).filter(Plant.category == category).all()

    def create(self, data):
        plant = Plant(**data)
        self.session.add(plant)
        self.session.commit()

    def create_from_obj(self, obj):
        self.session.add(obj)
        self.session.commit()

    def create_all(self, objs):
        self.session.add_all(*objs)
        self.session.commit()



    def delete(self, name):
        plant = self.session.query(Plant).filter_by(name=name).first()
        self.session.delete(plant)
        self.session.commit()