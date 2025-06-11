import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator

#engine = create_engine(os.environ["DATABASE_URL"])

## class that handles the connection with the sql server
class SQLconnection:

    def __init__(self):
        ## we create an engine with the url connection
        self.engine = create_engine(url = "postgresql+psycopg2://postgres:postgres@localhost:5432/finance_db", echo=True) 

        print("Connecting to DB...")
        print(self.engine.url)

        self.Base = declarative_base()
        self.sessionmaker = sessionmaker(self.engine)

    ## function that yields a session
    def get_session(self) -> Generator[Session, None, None]: 

        session : Session  = self.sessionmaker()
        try:
            yield session
        finally:
            session.close()