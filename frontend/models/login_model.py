import requests
from  requests import Response
import logging
from models.model import Model

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
handler = logging.StreamHandler()  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
        

class LoginModel(Model):
        
    def post_login(self, payload : dict[str, str]) -> Response:
        
        response = requests.post(f"{self.url}/user/login", json=payload) 
        
        logger.debug(f"send post request for credentials {payload}, retrieved: {response.json() if response.status_code == 200 else response.text}")
        
        return response
    
    def post_logout(self):
        
        logger.debug(f"logging out the user")
        
        response = requests.post(f"{self.url}/user/logout", auth=self.token_auth)
        
        logger.debug(f"logout status : {response.status_code}")
        
        