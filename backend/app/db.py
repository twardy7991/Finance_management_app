from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator
from sqlalchemy import orm
from contextlib import contextmanager
#engine = create_engine(os.environ["DATABASE_URL"])

## class that handles the connection with the sql server

#  

Base = declarative_base()

class Database:

    def __init__(self, db_url : str):
        
        ## we create an engine with the url connection
        self._engine = create_engine(url = db_url, echo=True) 

        print("Connecting to DB...")
        print(self._engine.url)

        self.Base = declarative_base()
        
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    ## function that yields a session
    @contextmanager
    def session(self): #-> Generator[Session, None, None] 

        session: Session = self._session_factory()
        
        try:
            yield session
        except Exception as e:
            session.rollback()
            print(f"Wystąpił błąd {e}")
        finally:
            session.close()