from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import streamlit as st
import os

# Streamlit Cloud secrets first, local .env fallback
try:
    DATABASE_URL = st.secrets["DATABASE_URL"]
except Exception:
    DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()