from sqlalchemy import select 
from app.db import SQLconnection
from app.database.models.models import Operation
from sqlalchemy.orm import Session

class DataService:

    def __init__(self, session: Session):
        self.session = session
        
    def get_user_finance_data(self, userid : int):
        
        stmt = select(Operation).where(Operation.user_id == userid)

        with self.session.begin() as session:

            result = self.session.scalars(stmt)
            
            values = []
            for e in result:
                print(e)

        return values



