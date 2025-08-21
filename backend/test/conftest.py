import sys

sys.path.append("/home/twardy/projects/Finance_calc/backend")

from sqlalchemy import Transaction, Connection
import pytest
from app.db import Database
import yaml
from contextlib import contextmanager

from app.db import Database
from app.auth.auth import AuthenticationTools
from app.services.utils.unit import UnitOfWorkUser, UnitOfWorkRegistration, UnitOfWorkCredential, UnitOfWorkOperation, UnitOfWorkSession
from app.services import SessionService, DataService, AuthenticationService, UserService


@pytest.fixture
def db():
    with open("config/config.yml", "r") as f:
        config = yaml.safe_load(f) 

    db = Database(db_url=config["db"]["url"])

    db.check_connection()
    return db

@pytest.fixture
def db_auth():
    with open("config/config.yml", "r") as f:
        config = yaml.safe_load(f) 

    db = Database(db_url=config["db_auth"]["url"])

    db.check_connection()
    return db

@pytest.fixture
def session(db : Database):
    connection : Connection = db.create_connection()
    transaction : Transaction = connection.begin() 
    
    try:
        session = db.get_session(connection)
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def session_auth(db_auth : Database):
    connection : Connection = db_auth.create_connection()
    transaction : Transaction = connection.begin() 
    
    try:
        session = db_auth.get_session(connection)
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def auth_tools():
    auth_tools = AuthenticationTools()
    return auth_tools

@pytest.fixture
def connection(db : Database):
    connection = db.create_connection()
    yield connection
    connection.close()
 
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
def session_factory_auth(db_auth : Database):
    connection : Connection = db_auth.create_connection()
    transaction : Transaction = connection.begin() 
    
    def _session_factory():
        session = db_auth.get_session(connection)
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
def session_uow(session_factory_auth):
    uow = UnitOfWorkSession(session_factory=session_factory_auth)
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

@pytest.fixture
def session_service(session_uow, auth_tools):
    service = SessionService(session_uow=session_uow, auth_tools=auth_tools)
    return service
