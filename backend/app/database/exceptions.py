### EXCEPTIONS FOR REPOSITORIES ###

class NotFound(Exception):
    
    entity: str
    
    def __init__(self, entity):
        super().__init__(f"{self.entity} not found")

class DataNotFound(NotFound):
    
    entity: str = "Data"

class UserNotProvidedError(Exception):
    def __init__(self):
        super().__init__("user_id was not provided")
        
class UserNotSavedError(Exception):
    def __init__(self):
        super().__init__("user was not saved to the database")
