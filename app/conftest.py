# https://johncox-38620.medium.com/creating-a-test-database-pytest-sqlalchemy-97356f2f02d2
import os
import pytest
from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import ProgrammingError, OperationalError
from sqlalchemy.orm import sessionmaker

from api.db import Base
from app.api.models.product import Product

load_dotenv()
TEST_DB_NAME = f'{os.getenv("DB_NAME")}_test'

url = URL.create(
    "mysql+mysqlconnector",
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host="localhost",
    database=TEST_DB_NAME,
    port=3306,
)


def drop_create_test_db():
    # Create connection string without specify which database
    engine = create_engine(
        URL.create(
            "mysql+mysqlconnector",
            username=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            host="localhost",
            port=3306,
        )
    )

    try:
        with engine.connect() as conn:
            conn = conn.execution_options(autocommit=False)
            try:
                conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
            except ProgrammingError:
                print("Could not drop the database, probably does not exist.")
            except OperationalError:
                print(
                    "Could not drop database because it’s being accessed by other users"
                )

            conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME}"))
    except Exception as e:
        print(f"Some other error", e)


@pytest.fixture(scope="session", autouse=True)
def db_session():
    engine = create_engine(url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()

    print(f"{TEST_DB_NAME} is ready")
    yield db_session
    db_session.rollback()
    db_session.close()
    drop_create_test_db()


@pytest.fixture(scope="session")
def seed(db_session):
    db_session.add_all(
        [
            Product(
                id=0,
                title="hello world",
                current_price=2.5,
                color="",
                size="",
                is_active=True,
                quantity=15,
            ),
            Product(
                id=1,
                title="toilet toy",
                current_price=7.99,
                color="",
                size="",
                is_active=True,
                quantity=5,
            )
        ]
    )
    db_session.commit()
