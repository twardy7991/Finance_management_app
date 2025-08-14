import sys

sys.path.append("/home/twardy/projects/Finance_calc/backend")

from sqlalchemy import Transaction, Connection
import pytest
from app.db import Database
import yaml
from contextlib import contextmanager

@pytest.fixture
def db():
    with open("config/config.yml", "r") as f:
        config = yaml.safe_load(f) 

    db = Database(db_url=config["db"]["url"])

    db.check_connection()
    return db

@pytest.fixture
def connection(db : Database):
    connection = db.create_connection()
    yield connection
    connection.close()

@pytest.fixture
def session(db : Database):
    connection : Connection = db.create_connection()
    transaction : Transaction = connection.begin() 
    
    @contextmanager
    def _session():
        try:
            session = db.get_session(connection)
            yield session
        finally:
            session.close()
            
    yield _session
    
    transaction.rollback()
    connection.close()
    
    