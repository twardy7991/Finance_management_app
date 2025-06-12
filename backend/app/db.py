from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator

#engine = create_engine(os.environ["DATABASE_URL"])

## class that handles the connection with the sql server

#  
class Database:

    def __init__(self, db_url : str):
        
        ## we create an engine with the url connection
        self.engine = create_engine(url = db_url, echo=True) 

        print("Connecting to DB...")
        print(self.engine.url)

        self.Base = declarative_base()
        self.sessionmaker = sessionmaker(self.engine)

    ## function that yields a session
    def get_session(self) -> Generator[Session, None, None]: 

        session : Session  = self.sessionmaker()
        
        try:
            yield session
        except Exception as e:
            session.rollback()
            print(f"Wystąpił błąd {e}")
        finally:
            session.close()