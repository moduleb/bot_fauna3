from app.database import session
from app.services.plant import PlantService
from app.services.user import UserService

plant_service = PlantService(session)
user_service = UserService(session)