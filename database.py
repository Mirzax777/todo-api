import psycopg
from psycopg.rows import dict_row
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database connection credentials
DB_HOST = "localhost"
DB_NAME = "todo-api"
DB_USER = "postgres"
DB_PASS = "Mirza"

# =============================================================================
# 1. ORM SETUP (SQLAlchemy)
# =============================================================================
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to yield database sessions in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =============================================================================
# 2. RAW SQL SETUP (psycopg v3)
# =============================================================================
def get_db_connection():
    """Returns a direct psycopg connection returning results as dictionaries."""
    return psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        row_factory=dict_row,
    )