from app.database.repositories import Repository
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from app.database.repositories import UserRepository, CredentialRepository

class UnitOfWorkBase(ABC):
    
    def __enter__(self):
        return self    

    def __exit__(self, exc_type, exc_value, traceback):
        self.rollback()
        
    @abstractmethod
    def commit(self):
        raise NotImplementedError()
    
    @abstractmethod
    def rollback(self):
        raise NotImplementedError()

class UnitOfWorkRegistration(UnitOfWorkBase):
    
    def __init__(self, session_factory):
            self._session_factory = session_factory

    def __enter__(self):
        self._session : Session = self._session_factory()
        self.credential_repository = CredentialRepository(self._session_factory, self._session)
        self.user_repository = UserRepository(self._session_factory, self._session)
        return super().__enter__()
    
    def commit(self):
        self._session.commit()
    
    def rollback(self):
        self._session.rollback()
    