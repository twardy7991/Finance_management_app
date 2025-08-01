from typing import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, text, Connection, orm
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from fastapi import HTTPException

Base = declarative_base()

### CLASS THAT HANDLES CONNECTION WITH DATABASE ###

class Database:

    def __init__(self, db_url : str):
        print("DB URL received:", db_url)
        self._engine = create_engine(url = db_url, echo=True) 

        print("Connecting to DB...")
        print(self._engine.url)

        self.Base = declarative_base()
        
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=True,
                bind=self._engine,
            ),
        )
    
    def check_connection(self) -> None:
        try:
            with self._engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Database connection successful.")
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
            raise ConnectionError("Database not available.") from e
    
    # used in testing 
    def get_session(self,  connection) -> Session:
        session_factory = orm.sessionmaker(
                autocommit=False,
                autoflush=True,
                bind=connection,
            )
        return session_factory()

    # used in testing 
    def create_connection(self) -> Connection:
        return self._engine.connect()
        
    @contextmanager
    def session(self) -> Generator[Session, None, None]:

        session: orm.Session = self._session_factory()
        
        try:
            yield session
        except Exception as e:
            session.rollback()
            print(f"Wystąpił błąd {e}")
        except OperationalError:
            raise HTTPException(status_code=503, detail="Database unavailable")
        finally:
            session.close()
            
        