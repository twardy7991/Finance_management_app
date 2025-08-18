from contextlib import contextmanager

import pytest
from sqlalchemy import Connection, Transaction, orm

from app.db import Database
from app.auth.auth import AuthenticationTools
from app.services.utils.unit import UnitOfWorkUser, UnitOfWorkRegistration, UnitOfWorkCredential, UnitOfWorkOperation
from app.services.user_service import UserService
from app.services.authentication_service import AuthenticationService
from app.services.data_service import DataService

@pytest.fixture
def auth_tools():
    auth_tools = AuthenticationTools()
    return auth_tools

@pytest.fixture
def connection(db : Database):
    connection = db.create_connection()
    yield connection
    connection.close()

# @pytest.fixture
# def session_factory(connection : Connection):
#     session_factory = orm.sessionmaker(
#             autocommit=False,
#             autoflush=False,
#             bind=connection,
#     )
#     yield session_factory
    
@pytest.fixture
def session_factory(db : Database):
    connection : Connection = db.create_connection()
    transaction : Transaction = connection.begin() 
    
    def _session_factory():
        session = db.get_session(connection)
        return session

            
    yield _session_factory
    
    transaction.rollback()
    connection.close()

@pytest.fixture
def uow_registration(session_factory):
    uow = UnitOfWorkRegistration(session_factory=session_factory)
    return uow

@pytest.fixture
def user_uow(session_factory):
    return UnitOfWorkUser(session_factory=session_factory)

@pytest.fixture
def credential_uow(session_factory):
    uow = UnitOfWorkCredential(session_factory=session_factory)
    return uow

@pytest.fixture
def operation_uow(session_factory):
    uow = UnitOfWorkOperation(session_factory=session_factory)
    return uow

@pytest.fixture
def authentication_service(auth_tools, credential_uow):
    service = AuthenticationService(auth_tools=auth_tools, credential_uow=credential_uow)
    return service

@pytest.fixture
def user_service(uow_registration, auth_tools, user_uow):
    service = UserService(uow_registration=uow_registration, 
                          auth_tools=auth_tools,
                          user_uow=user_uow)
    return service

@pytest.fixture
def data_service(operation_uow):
    service = DataService(operation_uow=operation_uow)
    return service
