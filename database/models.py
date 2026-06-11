import uuid

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.connection import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(
        String(150),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    country = Column(String(100))

    team = Column(String(100))

    role = Column(
        String(20),
        nullable=False,
        default="user"
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    predictions = relationship(
        "Prediction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    winner_prediction = relationship(
    "WinnerPrediction",
    uselist=False,
    cascade="all, delete-orphan"
    )


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = {"extend_existing": True}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    stage = Column(
        String(50),
        nullable=False
    )

    group_name = Column(
        String(20)
    )

    match_date = Column(
        DateTime(timezone=True),
        nullable=False
    )

    home_team = Column(
        String(100),
        nullable=False
    )

    away_team = Column(
        String(100),
        nullable=False
    )

    stadium = Column(
        String(200)
    )

    city = Column(
        String(100)
    )

    home_score = Column(
        Integer
    )

    away_score = Column(
        Integer
    )

    status = Column(
        String(20),
        nullable=False,
        default="scheduled"
    )

    created_by_admin = Column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    predictions = relationship(
        "Prediction",
        back_populates="match",
        cascade="all, delete-orphan"
    )



class Prediction(Base):
    __tablename__ = "predictions"
    __table_args__ = {"extend_existing": True}
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "match_id",
            name="uq_user_match"
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    match_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "matches.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    predicted_home_score = Column(
        Integer,
        nullable=False
    )

    predicted_away_score = Column(
        Integer,
        nullable=False
    )

    points_earned = Column(
        Integer,
        nullable=False,
        default=0
    )


    is_exact_score = Column(
        Boolean,
        nullable=False,
        default=False
    )

    is_correct_result = Column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship(
        "User",
        back_populates="predictions"
    )

    match = relationship(
        "Match",
        back_populates="predictions"
    )


class WinnerPrediction(Base):
    __tablename__ = "winner_predictions"
    __table_args__ = {"extend_existing": True}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True
    )

    predicted_winner = Column(
        String(100),
        nullable=False
    )

    prediction_stage = Column(
        String(50),
        nullable=False
    )

    bonus_points = Column(
        Integer,
        nullable=False,
        default=0
    )

    bonus_awarded = Column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship("User")