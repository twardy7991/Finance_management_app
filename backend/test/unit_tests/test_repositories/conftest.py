from typing import Generator

import pytest

from app.database.repositories import UserRepository, CredentialRepository, DataRepository, SessionRepository

@pytest.fixture
def user_repository(session) -> UserRepository:
    repository = UserRepository(session=session)
    return repository
    
@pytest.fixture
def credential_repository(session) -> CredentialRepository:
    repository = CredentialRepository(session=session)
    return repository

@pytest.fixture
def data_repository(session):
    data_repository = DataRepository(session=session)
    return data_repository
    
@pytest.fixture
def session_repository(session_auth) -> SessionRepository:
    session_repository = SessionRepository(session=session_auth)
    return session_repository