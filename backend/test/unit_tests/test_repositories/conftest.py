from typing import Generator

import pytest

from app.database.repositories import UserRepository, CredentialRepository, DataRepository

@pytest.fixture
def user_repository(session) -> Generator[UserRepository]:
    from app.database.repositories import UserRepository
    repository = UserRepository(session=session)
    yield repository
    
@pytest.fixture
def credential_repository(session) -> Generator[CredentialRepository]:
    from app.database.repositories import CredentialRepository
    repository = CredentialRepository(session=session)
    yield repository

@pytest.fixture
def data_repository(session):
    data_repository = DataRepository(session=session)
    yield data_repository