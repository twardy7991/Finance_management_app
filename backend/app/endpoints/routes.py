from fastapi import APIRouter, Depends
from app.database.controllers.data_service import DataService
from app.endpoints.schemas import UserId
from app.db import SQLconnection

connection = SQLconnection()

## we create funtion to point to the get_session from SQLconnection class so we can use it in Depends() 
## we create is outside the class as Depends() cannot use self.*** as it is in function parentheses
def get_session(): 
    yield from connection.get_session()

class Routing:

    def __init__(self):
        self.router = APIRouter()

    def get_data_service(self, session=Depends(get_session)):
        return DataService(session)

    def configure_routes(self): 

        @self.router.get("/")
        def root():
            return {"message": "Hello from FastAPI"}

        @self.router.post("/user/data")
        def get_user_finance_data(
            userid: UserId, 
            data_service : DataService = Depends(self.get_data_service)
            ):
            return data_service.get_user_finance_data(userid.user_id)
        
    