from datetime import date
from decimal import Decimal

from starlette.testclient import TestClient
import pytest
import yaml
from sqlalchemy import Transaction, Connection

from app.database.models import Operation
from app.containers import Container
from app.database.repositories import DataRepository, UserRepository
from contextlib import contextmanager
from app.main import create_app
from app.db import Database

class TestDatabase(Database):
    def __init__(self, db_url : str):
        super().__init__(db_url)
    
    @contextmanager
    def session(self):
        connection : Connection = super().create_connection()
        transaction : Transaction = connection.begin() 
        
        try:
            session = super().get_session(connection)
            yield session
        finally:
            session.close()
            transaction.rollback()
            connection.close()
            
@pytest.fixture
def client(container):
    app = create_app()
    app.container = container
    return TestClient(app)

@pytest.fixture
def container(session):
    with open("config/config.yml", "r") as f:
        config = yaml.safe_load(f) 
    
    database = TestDatabase(db_url=config["db"]["url"])
    container = Container()
    
    # container.data_repository.override(DataRepository(lambda: session))
    # container.user_repository.override(UserRepository(lambda: session))
    
    container.db.override(database)
    container.wire(modules=["app.endpoints.routes"])
    yield container
    container.unwire()

@pytest.fixture
def operations_to_save():

    return [
        Operation(
            operation_id=1,
            user_id=2,
            operation_date=date(2025, 2, 23),
            category="PRZELEW",
            description="ZUS ODDZIAŁ ŁÓDŹ  PRZELEW PRZYCHODZĄCY",
            value=Decimal("3500.00"),
            currency="PLN"
        ),
        Operation(
            operation_id=2,
            user_id=2,
            operation_date=date(2025, 2, 22),
            category="Transport i paliwo",
            description="SHELL STACJA PALIW 1234  ZAKUP PRZY UŻYCIU KARTY W KRAJU",
            value=Decimal("-239.99"),
            currency="PLN"
        ),
        Operation(
            operation_id=3,
            user_id=2,
            operation_date=date(2025, 2, 21),
            category="BLIK",
            description="ALLEGRO.PL PŁATNOŚĆ BLIK P2P",
            value=Decimal("-125.00"),
            currency="PLN"
        ),
        Operation(
            operation_id=4,
            user_id=2,
            operation_date=date(2025, 5, 18),
            category="Utilities",
            description="Electricity bill",
            value=Decimal("-65.75"),
            currency="USD"
        ),
        Operation(
            operation_id=5,
            user_id=2,
            operation_date=date(2025, 5, 19),
            category="Dining",
            description="Dinner at Luigi's",
            value=Decimal("-45.00"),
            currency="USD"
        ),
        Operation(
            operation_id=6,
            user_id=2,
            operation_date=date(2025, 5, 22),
            category="Health",
            description="Pharmacy purchase",
            value=Decimal("-22.10"),
            currency="USD"
        ),
    ]