from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from app.database.repositories import UserRepository, CredentialRepository, DataRepository

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

class UnitOfWorkCredential(UnitOfWorkBase):
    
    def __init__(self, session_factory):
        self._session_factory : Session = session_factory
        
    def __enter__(self):
        self._session : Session = self._session_factory()
        self.repository = CredentialRepository(session=self._session_factory())
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        return super().__exit__(exc_type, exc_value, traceback)
    
    def rollback(self):
        self._session.rollback()
    
    def commit(self):
        self._session.commit()
        
class UnitOfWorkUser(UnitOfWorkBase):
    
    def __init__(self, session_factory):
        self._session_factory : Session = session_factory
        
    def __enter__(self):
        self._session : Session = self._session_factory()
        self.repository = UserRepository(session=self._session_factory())
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        return super().__exit__(exc_type, exc_value, traceback)
    
    def rollback(self):
        self._session.rollback()
    
    def commit(self):
        self._session.commit()
        
class UnitOfWorkOperation(UnitOfWorkBase):
    
    def __init__(self, session_factory):
        self._session_factory : Session = session_factory
        
    def __enter__(self):
        self._session : Session = self._session_factory()
        self.repository = DataRepository(session=self._session_factory())
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        return super().__exit__(exc_type, exc_value, traceback)
    
    def rollback(self):
        self._session.rollback()
    
    def commit(self):
        self._session.commit()
    
class UnitOfWorkRegistration(UnitOfWorkBase):
    
    def __init__(self, session_factory, ):
        self._session_factory : Session = session_factory

    def __enter__(self):
        self._session : Session = self._session_factory()
        self.credential_repository = CredentialRepository(self._session)
        self.user_repository = UserRepository(self._session)
        return super().__enter__()
    
    def commit(self):
        self._session.commit()
    
    def rollback(self):
        self._session.rollback()
    