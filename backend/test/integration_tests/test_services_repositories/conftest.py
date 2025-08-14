import pytest
from datetime import date
from decimal import Decimal
from app.database.models import Operation
from sqlalchemy import orm

@pytest.fixture
def auth_tools():
    from app.auth.auth import AuthenticationTools
    auth_tools = AuthenticationTools()
    return auth_tools

@pytest.fixture
def user_repository(session):
    from app.database.repositories import UserRepository
    repository = UserRepository(session_factory=session)
    return repository

@pytest.fixture
def credential_repository(session):
    from app.database.repositories import CredentialRepository
    repository = CredentialRepository(session_factory=session)
    return repository

@pytest.fixture
def authentication_service(credential_repository, auth_tools):
    from app.services.authentication_service import AuthenticationService
    service = AuthenticationService(credential_repository=credential_repository, auth_tools=auth_tools)
    return service

@pytest.fixture
def session_factory(connection):
    session_factory = orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=connection,
    )
    yield session_factory

@pytest.fixture
def uow_registration(session_factory):
    from app.services.utils.unit import UnitOfWorkRegistration
    with UnitOfWorkRegistration(session_factory=session_factory) as uow:
        yield uow

@pytest.fixture
def user_service(user_repository, uow_registration, auth_tools):
    from app.services.user_service import UserService
    service = UserService(user_repository=user_repository, 
                          uow_registration=uow_registration, 
                          auth_tools=auth_tools)
    return service

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

@pytest.fixture
def operations_in_database():
    
    return [
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
        )
    ]