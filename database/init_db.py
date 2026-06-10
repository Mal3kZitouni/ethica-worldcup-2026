from database.connection import engine, Base

# Import all models so SQLAlchemy knows about them
from database.models import (
    User,
    Match,
    Prediction,
    WinnerPrediction
)

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")