from typing import Generator

import pytest

from app.database.repositories import UserRepository, CredentialRepository

@pytest.fixture
def user_repository(session) -> Generator[UserRepository]:
    from app.database.repositories import UserRepository
    repository = UserRepository(session_factory=session)
    yield repository
    
@pytest.fixture
def credential_repository(session) -> Generator[CredentialRepository]:
    from app.database.repositories import CredentialRepository
    repository = CredentialRepository(session_factory=session)
    yield repository