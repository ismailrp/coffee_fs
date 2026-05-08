import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/coffeeapp"

MAX_RETRIES = 10
RETRY_DELAY = 3

for i in range(MAX_RETRIES):

    try:
        engine = create_engine(DATABASE_URL)

        connection = engine.connect()

        print("Database connected!")

        connection.close()

        break

    except Exception:

        print(f"Retry database connection {i+1}")

        time.sleep(RETRY_DELAY)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()