from models.login_model import LoginModel
from requests import Response
from app_state import AppState

class LoginViewModel:
    
    def __init__(self, model : LoginModel, app_state : AppState):
        
        self.model = model
        self.logged = False
        self.login_message = ""
        self.app_state = app_state
        
    def login(self, username : str, password : str) -> None:
        
        if username == "":
            username = "user3"
            password = "password2"
            
        credentials : dict[str, str] = {
            "username" : username,
            "password" : password
        }
        
        response = self.model.post_login(credentials)
        
        if response.status_code == 200:
            self.logged = True
            self.app_state.session_id = response.json()["session_id"]
            self.login_message = "Login Successful"
        else:
            self.login_message = "Login Unsuccessful"
        
    def logout(self):
        return self.model.post_logout()
    

    
    
        