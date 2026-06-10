from database.connection import Base, engine
from database.models import User, Match, Prediction

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")