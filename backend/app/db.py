from typing import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, text, Connection, orm
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

### CLASS THAT HANDLES CONNECTION WITH DATABASE ###

class Database:

    def __init__(self, db_url : str, flush : bool = True):
        print("DB URL received:", db_url)
        self._engine = create_engine(url = db_url, echo=True) 

        print("Connecting to DB...")
        if not flush:
            print("Test instance")
        print(self._engine.url)

        self.Base = declarative_base()
        
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
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
        
    def session_factory(self) -> Session:
        # try:
            return self._session_factory
        # except Exception as e:
        #     session.rollback()
        #     print(f"Wystąpił błąd {e}")
        # except OperationalError:
        #     raise HTTPException(status_code=503, detail="Database unavailable")
        # finally:
        #     session.close()
            
        